import numpy as np
import DCParam as P

class ctrlPD:
    def __init__(self):
        ts = 0.01             # settling time, s
        zeta = 0.7          # damping ratio
        omega_n = 4.0 / ts    # natural frequency
        
        mod_d = 30
        mod_p = 1
        
        self.kd = 10
        self.kp = 5.0
        
        print (self.kd, self.kp)

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