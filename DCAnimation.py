import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import DCParam as P

class DCAnimation:
    def __init__(self):
        self.flagInit = True                  # Used to indicate initialization
        self.fig, self.ax = plt.subplots()    # Initializes a figure and axes object
        self.handle = []                      # Initializes a list object that will
                                            # be used to contain handles to the
                                            # patches and line objects.
        self.length=P.length
        self.width=P.width
        plt.axis([-P.length-P.length/5, 2*P.length, -P.length, 2*P.length]) # Change the x,y axis limits
        plt.plot([-P.length-P.length/5,2*P.length],[0,0],'k--')    # Draw track
        plt.plot([-P.length, -P.length], [0, 2*P.width], 'k')  # Draw wall