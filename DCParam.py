# DC Motor Parameter File
import numpy as np 

# Physical parameters of the arm known to the controller
radius = (7.3 / 100) / (2.0)    # radius of the wheel, cm -> m4
m = 13                          # mass of the wheel, g
d = (2.5 / 100)                 # thickness of the wheel, mm -> m

# Parameters for the motor
vMax = 3                    # rated voltage of the motor can go up to 12V DC, but max operation should be 3 V
thetadotMax = 6600          # maximum no load angular velocity, rpm
mMotor = 26                 # mass of motor, g

# Parameters for animation
length = (2.0 / 10)         # length of the base, cm -> m
width = (1.0 / 10)          # width of the base, cm -> m

figWidth = 1.0              # width of plot, m
figHeight = 1.0             # width of plot, m

# Initial conditions
theta0 = 0.0                # initial wheel angle, rad
thetadot0 = 0.0             # initial wheel angular velocity, rad/s

# Calculations
R = 3.75                                            # Ohms
kt = vMax / ((thetadotMax * 2 * np.pi) / 60)        # torque constant

# Simulation parameters
t_start = 0.0               # Start time of simulation
t_end = 50.0                # End time of simulation
Ts = 0.01                   # sample time for simulation
t_plot = 0.1                # the plotting and animation is updated at this rate