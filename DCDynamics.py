import numpy as np 
import DCParam as P


class DCDynamics:
    def __init__(self, alpha=0.0):
        # Initial state conditions
        self.state = np.array([
            [P.theta0],      # initial angle
            [P.thetadot0]    # initial angular rate
        ])  
        self.m = P.m # mass of wheel

        self.radius = P.radius # radius of wheel

        self.d = P.d # thickness of wheel
        
        self.Ts = P.Ts  
        self.torque_limit = P.tau_max

    def update(self, u):
        # This is the external method that takes the input u at time
        # t and returns the output y at time t.
        # saturate the input torque
        # u = saturate(u, self.torque_limit)
        self.rk4_step(u)  # propagate the state by one time sample
        y = self.h()  # return the corresponding output
        return y

    def f(self, state, voltage):
        # Return xdot = f(x,u), the system state update equations
        # re-label states for readability
        theta = state[0][0]
        thetadot = state[1][0]
        thetaddot = 
        xdot = np.array([[thetadot], [thetaddot]])
        return xdot

    def h(self):
        # return the output equations
        # could also use input u if needed
        theta = self.state[0][0]
        y = np.array([[theta]])
        return y

    def rk4_step(self, u):
        # Integrate ODE using Runge-Kutta RK4 algorithm
        F1 = self.f(self.state, u)
        F2 = self.f(self.state + self.Ts / 2 * F1, u)
        F3 = self.f(self.state + self.Ts / 2 * F2, u)
        F4 = self.f(self.state + self.Ts * F3, u)
        self.state = self.state + self.Ts / 6 * (F1 + 2 * F2 + 2 * F3 + F4)

'''
def saturate(u, limit):
    if abs(u) > limit:
        u = limit * np.sign(u)
    return u
'''