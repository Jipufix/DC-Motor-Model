import numpy as np
import DCParam as P

class ctrlPD:
    def __init__(self):
        ts = 0.01              # settling time, s
        
        self.kd = (1.0 - P.R * P.m * (P.radius**2)) / (2.0 * P.kt)
        self.kp = (2.0 / (ts * P.kt)) - 1.0

    def update(self, thetadot_r, state):
        thetadot = state[1][0]
        thetaddot = state[2][0]
        V_tilde = (self.kp * (thetadot_r - thetadot)) - (self.kd * thetaddot)
        V_tilde = saturate(V_tilde, P.VMax)
        return V_tilde
    
def saturate(u, limit):
    if abs(u) > limit:
        u = limit * np.sign(u)
    return u