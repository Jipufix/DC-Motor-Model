# DC Motor Parameter File
import numpy as np 

# Physical parameters of the arm known to the controller
radius = (7.3 / 100) / (2.0)        # radius of the wheel, cm -> m
m = 13.0 / 1000.0                       # mass of the wheel, g -> kg

# Parameters for the motor
VMax = 9.0                           # rated voltage of the motor can go up to 12V DC, but max operation should be 3 V
thetadotMax = 5280                  # maximum no load angular velocity, rpm
mMotor = 26 / 1000                  # mass of motor, g -> kg

# Parameters for animation
length = (2.0 / 100)         # length of the base, cm -> m
width = (1.0 / 100)          # width of the base, cm -> m

figWidth = 1.0              # width of plot, m
figHeight = 1.0             # width of plot, m

# Initial conditions
theta0 = 0.0                # initial wheel angle, rad
thetadot0 = 0.0             # initial wheel angular velocity, rad/s
thetaddot0 = 0.0            # initial wheel angular acceleration, rad/s^2

# Calculations
R = VMax / 0.11                                     # Ohms
kt = VMax / ((thetadotMax * 2 * np.pi) / 60)        # torque constant

# Simulation parameters
t_start = 0.0               # Start time of simulation
t_end = 100.0                # End time of simulation
Ts = 0.01                   # sample time for simulation
t_plot = 0.1                # the plotting and animation is updated at this rate