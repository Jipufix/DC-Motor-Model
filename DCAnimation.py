import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import DCParam as P

class DCAnimation:
    def __init__(self):
        self.flagInit = True                    # Used to indicate initialization
        self.fig, self.ax = plt.subplots()      # Initializes a figure and axes object
        self.handle = []                        # Initializes a list object that will
                                                    # be used to contain handles to the
                                                    # patches and line objects.
        
        # Get figure size in inches and convert to pixels
        self.figWidth = P.figWidth
        self.figHeight = P.figHeight
        
        self.length = P.length
        self.width = P.width
        self.radius = P.radius
        
        self.x = (self.figWidth / 2.0) 
        self.y = (self.figWidth / 2.0) 
        
    def update(self, u):
        # Process inputs to function
        theta = u[0][0]     # angular offset from initial wheel position, rad
        self.drawWheel(theta)
        
        if (self.flagInit):
            self.flagInit = False
    
    def drawBase(self):
        # only get drawn once
        if (self.flagInit):
            # Create the rectangle for the base
            base = mpatches.Rectangle([self.x, self.y], self.length, self.width, fc='gray', ec='black')
            # Add the patch to the handle list
            self.handle.append(base)
            # Add the patch to the plot
            self.ax.add_patch(base)
    
    def drawWheel(self, theta):
        # define the radius of the wheel
        pointRadius = 0.01
        
        # Circle is unmoving, only defined point moves
        if (self.flagInit):
            # create a wheel
                # [x, y] = center of the circle
                # fc = face color, ec = edge color
            wheel = mpatches.Circle([self.x, self.y], self.radius, fc='blue', ec='black')
            self.handle.append(wheel)
            self.ax.add_patch(wheel)
        
        # update the point position
        xPoint = self.x + (self.radius * np.cos(theta))
        yPoint = self.y + (self.radius * np.sin(theta))
        # add a point at the marked coordinates
        point = mpatches.Circle([xPoint, yPoint], pointRadius, fc='red', ec='red')
        self.handle.append(point)
        self.ax.add_patch(point)
