import nidaqmx
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time
from scipy.signal import find_peaks  # For detecting peaks in data
import pandas as pd


################################################################################################
############# These are the two functions you need to update
################################################################################################

def create_reference():
    """Generate a reference input signal."""
    # repeat a list using the * operator. Example: [5]*4 turns into [5,5,5,5]
    # combine two lists using the + operator. Example: [1,2]+[3,4] = [1,2,3,4]
    
    reference_signal = [0]*20+[6000]*50 # classic step function 
    # TODO: play around with other references
    # reference_signal = gen_sin(100,0.01,4000) # sinusoidal reference
    
    return reference_signal


def determine_control_output(error):
    """Determine control output based on error (replace this with your control logic)."""
    
    # NOTE: control_output should be a desired change in voltage (equivalent to the ~ variables calculated in lab simulations)

    control_output = 0 # TODO: change this! 

    return control_output


################################################################################################
############# DO NOT make any changes to the functions below w/o clearing with Dr. Kimball first
################################################################################################


def moving_average_list(lst, window_size):
    """
    Calculates the moving average of a list of numbers.

    Parameters:
    lst (list of float): The input list of numbers.
    window_size (int): The window size for calculating the moving average.

    Returns:
    list of float: A list containing the moving average values.
    """
    if not lst:
        raise ValueError("Input list is empty.")
    
    if window_size < 1:
        raise ValueError("Window size must be at least 1.")
    
    if window_size > len(lst):
        raise ValueError("Window size cannot be larger than the list length.")
    
    half_window = window_size // 2
    
    # Add buffer to the start and end of the list
    padded_lst = [lst[0]] * half_window + lst + [lst[-1]] * half_window

    moving_averages = []
    for i in range(len(lst)):
        window_sum = sum(padded_lst[i:i + window_size])
        moving_averages.append(window_sum / window_size)
    
    return moving_averages


def filter_lists(list1, list2, threshold):
    """
    Filters out values from two lists based on a threshold applied to the first list.

    Parameters:
    list1 (list of floats/ints): The first list to apply the threshold to.
    list2 (list of any type): The second list to filter in parallel with the first list.
    threshold (float/int): The threshold value for filtering.

    Returns:
    tuple: Two lists with filtered values.
    """
    if len(list1) != len(list2):
        print("list 1 length: ", len(list1))
        print("list 2 length: ", len(list2))
        raise ValueError("Both lists must have the same length.")

    filtered_list1 = []
    filtered_list2 = []
    
    for value1, value2 in zip(list1, list2):
        if value1 <= threshold:
            filtered_list1.append(value1)
            filtered_list2.append(value2)
    
    return filtered_list1, filtered_list2


def gen_sin(duration, freq, amp):
    # returns list A*sin(2*pi*f*t)
    T = range(0,duration)
    sinusoid = [amp*np.sin(2*np.pi*freq*t) for t in T]
    return sinusoid


def calculate_rpm(analog_input, last_rpm, voltage_sign):
    """Calculate RPM based on analog input data."""
    # NOTE: minimum rpm reliably detected dictated by length of analog input. 
    photo_inv = analog_input # inverting no longer necessary [x*-1 for x in analog_input] # best peaks are inverted, invert the analog signal to find 
    diff_photo = np.diff(photo_inv) # quick high pass filter
    peaks, _ = find_peaks(diff_photo, prominence=0.02) # find rising edges from original waveform 

    peak_intervals = np.diff(peaks)
    rpms = [float((sampling_rate * 60) / x) for x in peak_intervals] # rotation per samples (1/peak_intervals) * samples per second * seconds per minute
    # quick cleanup of rpms before applying moving average 
    rpms, samples = filter_lists(rpms, peaks[:-1], 10000) 

    if(len(rpms)>0):
        rpm_final = rpms[-1] # np.median(rpms) # np.mean(rpms) # take average rpms[-1] # take the last value as the most recent RPM
    else:
        rpm_final = 0


    # add a sign to the rpm value

    # case: RPMs are 0, then should match voltage sign as soon as it starts moving. 
    # RPMs increasing, match the voltage sign. 
    # RPMs decreasing could be a lower abs(voltage) or a voltage sign change. 
    # RPM sign change happens when RPMs go back to 0 and then start increasing again, at which point they match the voltage sign. 

    # simplest rule: if RPMs are increasing, the sign matches the voltage sign. 

    rpm_diff = rpm_final - abs(last_rpm) # remove the sign on the last RPM calculated since rpm_final doesn't have a sign yet 
    
    if(np.sign(rpm_diff) == 1): # if rpms are increasing, match voltage sign. 
        rpm_final = rpm_final * voltage_sign
    else: # match prior RPM sign
        if(last_rpm < 0): # don't want to use np.sign() function because that will give weird behavior when prior rpm is 0
            rpm_final = rpm_final * -1

    return rpm_final


def update_motor_speed(control_output,last_command):
    """Update motor speed using control output and last command."""

    global voltage_sign

    # determine magnitude of voltage command
    volts = last_command + control_output

    # saturate based on max_voltage
    if volts > max_voltage:
        volts = max_voltage
    elif volts < -max_voltage:
        volts = -max_voltage

    # translate to pwm 
    pwm_percent = abs(round(volts/max_voltage,2)) # limit to 2 decimal places

    # determine direction. Always send command, even if redundant (ensures predictable run time)
    if volts < 0:
        # set the motor to spin backward
        set_pin_state(1, False)  # Set pin 1 high
        set_pin_state(2, True)  # Set pin 2 low   

        voltage_sign = -1 # update flag for rpms
    else:
        # set the motor to spin forward
        set_pin_state(1, True)  # Set pin 1 high
        set_pin_state(2, False)  # Set pin 2 low    

        voltage_sign = 1 # update flag for rpms

    # send new pwm command to motor
    pwm_control(pin=0, frequency=50, duty_cycle=pwm_percent, duration=0.1) 

    return volts


def update_plot():
    global i
    global voltage_sign
    global rpm_values
    global window_size
    
    if i < reference_duration:
        # 1. Read the reference value
        reference_value = reference_signal[i]

        # 2. Calculate RPM from analog input
        analog_input = task.read(number_of_samples_per_channel=int(sampling_rate / 4)) # Prior: / 10

        all_analog_data.extend(analog_input)

        rpm_value = calculate_rpm(analog_input,rpm_values[-1],voltage_sign)

        # 3. Calculate error
        error = reference_value - rpm_value

        # 4. Determine control output
        control_output = determine_control_output(error)

        # 5. Update motor speed
        voltage_input = update_motor_speed(control_output,control_values[-1])

        # Log data for plotting
        current_time = time.time() - start_time
        times.append(current_time)
        ref_values.append(reference_value)
        rpm_values.append(rpm_value)
        control_values.append(voltage_input)
        
        # Limit data to window size
        if current_time > window_size:
            start_idx = np.searchsorted(times, current_time - window_size)
            times_plot = times[start_idx:]
            ref_values_plot = ref_values[start_idx:]
            rpm_values_plot = rpm_values[start_idx:]
            control_values_plot = control_values[start_idx:]
        else:
            times_plot = times
            ref_values_plot = ref_values
            rpm_values_plot = rpm_values
            control_values_plot = control_values

        # Update plots with limited data
        ref_line.set_data(times_plot, ref_values_plot)
        rpm_line.set_data(times_plot, rpm_values_plot)
        control_line.set_data(times_plot, control_values_plot)

        ax1.relim()
        ax1.autoscale_view()
        ax2.relim()
        ax2.autoscale_view()

        canvas.draw()

        # Move to next index
        i += 1
        root.after(int(1000 / sampling_rate), update_plot)

    else:
        plt.close(fig) # close the updating figure
        root.destroy() # close the GUI


def plot_full_data():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))  # Create two subplots

    # First subplot: RPM vs Reference
    ax1.plot(times, ref_values, label='Reference')
    ax1.plot(times, rpm_values, label='RPM')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('RPM')
    ax1.legend()
    ax1.set_title('Reference vs RPM')
    ax1.grid(True)

    # Second subplot: Control Output
    ax2.plot(times, control_values, label='Control Output', color='orange')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Control Output')
    ax2.set_title('Control Output over Time')
    ax2.grid(True)

    plt.tight_layout()  # Adjust layout to prevent overlap
    plt.savefig('rpm_control_data.png')
    plt.show()


def set_pin_state(pin, state):
    # sets myDAQ Digitial I/O pin state 
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(f'myDAQ1/port0/line{pin}')
        task.write([state])


def pwm_control(pin=0, frequency=1, duty_cycle=0.5, duration=5):
    # print("duty cycle: ",duty_cycle)
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(f'myDAQ1/port0/line{pin}')

        start_time = time.time()
        period = 1 / frequency

        while (time.time() - start_time) < duration:
            if(duty_cycle > 0): # will turn on otherwise!
                # High signal
                task.write([True])
                time.sleep(duty_cycle * period)

            # Low signal
            task.write([False])
            time.sleep((1 - duty_cycle) * period)




################################################################################################
############# TODO: make sure this matches your setup Don't change the rest! 
################################################################################################

voltage_source = 9.0 # should be 9 volt battery or 12 V plug. 

################################################################################################
############# Setup GUI and hardware, initialize global variables, run script, shut down
################################################################################################

max_voltage = voltage_source - 2.0  # Maximum voltage able to send to the motor 


# Set up reference and timing
reference_signal = create_reference()

reference_duration = len(reference_signal)
sampling_rate = 1000  # Hz
window_size = 5      # seconds of data to display
duration = window_size 
buffer_size = int(sampling_rate * duration)
channels = ["myDAQ1/ai0"] #["myDAQ1/ai0", "myDAQ1/ai1"]  # List of analog channels to record from

# Tkinter setup
root = tk.Tk()
root.title("Motor Control GUI")

# Set up the Matplotlib plots in Tkinter
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Plot placeholders
ref_line, = ax1.plot([], [], label='Reference')
rpm_line, = ax1.plot([], [], label='RPM')
control_line, = ax2.plot([], [], label='Control Output')
ax1.set_title('Reference and RPM')
ax2.set_title('Control Output')
ax1.legend()
ax2.legend()

# Initialize global variables
times = [0]
ref_values = [0]
rpm_values = [0]
control_values = [0]
all_analog_data = []

# Create a task to set up analog channels
task = nidaqmx.Task()
for channel in channels:
    task.ai_channels.add_ai_voltage_chan(channel)
task.timing.cfg_samp_clk_timing(sampling_rate)

# turn on LED and Photodiode circuits 
set_pin_state(3, True)  # Set pin 1 low

# Main loop
start_time = time.time()
i = 0  # Reference index
voltage_sign = 1 # 1 indicates voltage is positive or 0. -1 indicates voltage is negative. 

# Start the update loop
update_plot()

# Run the Tkinter main loop
root.mainloop()

# Create a figure with the full results
plot_full_data()

# Calculate error from the run, print to command line 
all_error = sum([abs(x-y) for x,y in zip(ref_values,rpm_values)])
print("Total error for this run was: ", all_error)

# turn off the motor
set_pin_state(1, False)  # Set pin 1 low
set_pin_state(2, False)  # Set pin 2 low  

# turn off LED and Photodiode circuits 
set_pin_state(3, False)  # Set pin 1 low

# Close the task when done
task.close()




