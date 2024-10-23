import matplotlib.pyplot as plt
import numpy as np
import DCParam as P
from signalGenerator import signalGenerator
from DCAnimation import DCAnimation
from dataPlotter import dataPlotter

# Instantiate the reference input classes
reference = signalGenerator(amplitude=0.5, frequency=0.1)
thetaRef = signalGenerator(amplitude=0.25*np.pi, frequency=0.1)
fRef = signalGenerator(amplitude=0.25, frequency=0.1)

# Instantiate teh simulation plots and animation 
dataPlot = dataPlotter()
animation = DCAnimation()

t = P.t_start  # time starts at t_start
while t < P.t_end:
    # set variables
    r = reference.square(t)
    theta = thetaRef.sin(t)
    f = fRef.sawtooth(t)
    
    # update animation
    state = np.array([[theta], [0.0]])
    animation.update(state)
    dataPlot.update(t, r, state, f)
    
    t = t + P.t_plot
    plt.pause(0.05)
    
# Keeps the program from closing unitl the user presses a button
print('Press key to close')
plt.waitforbuttonpress()
plt.close()
