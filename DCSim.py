import matplotlib.pyplot as plt
import numpy as np
import DCParam as P
from signalGenerator import signalGenerator
from DCAnimation import DCAnimation
from dataPlotter import dataPlotter
from DCDynamics import DCDynamics
from ctrlPD import ctrlPD

# Instantiate the reference input classes
DC = DCDynamics()
controller = ctrlPD()
reference = signalGenerator(amplitude=500, frequency=0.05)


# Instantiate teh simulation plots and animation 
dataPlot = dataPlotter()
animation = DCAnimation()

t = P.t_start  # time starts at t_start
while t < P.t_end:  # main simulation loop
    # Propagate dynamics in between plot samples
    t_next_plot = t + P.t_plot
    
    while t < t_next_plot:
        # set variables
        r = reference.square(t)      # convert to rad/s
        x = DC.state
        
        u = controller.update(r, x)
        print(x)
        y = DC.update(u)
        t = t + P.Ts

    # update animation
    animation.update(DC.state)
    dataPlot.update(t, r, x, u)
    # advance time by t_plot
    t = t + P.t_plot
    plt.pause(0.05)  # allow time for animation to draw
    
# Keeps the program from closing unitl the user presses a button
print('Press key to close')
plt.waitforbuttonpress()
plt.close()
