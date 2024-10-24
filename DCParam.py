# DC Motor Parameter File
import numpy as np 

# Physical parameters of the arm known to the controller
radius = 7.3 / (2.0 * 10)          # radius of the wheel, cm
m = 13                      # mass of the wheel, g
d = (2.5 / 100)              # thickness of the wheel, mm -> m

# Parameters for the motor
voltage = 12                # rated voltage of the motor can go up to 12V DC
mMotor = 26                 # mass of motor, g

# Parameters for animation
length = (2.0 / 10)         # length of the base, cm -> m
width = (1.0 / 10)          # width of the base, cm -> m

figWidth = 1.0              # width of plot, m
figHeight = 1.0             # width of plot, m

# Initial conditions
theta0 = 0.0                # initial wheel angle, rad
thetadot0 = 0.0             # initial wheel angular velocity, rad/s

# Simulation parameters
t_start = 0.0               # Start time of simulation
t_end = 50.0                # End time of simulation
Ts = 0.01                   # sample time for simulation
t_plot = 0.1                # the plotting and animation is updated at this rate