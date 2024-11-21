import numpy as np
import DCParam as P

class ctrlPD:
    def __init__(self):
        ####################################################
        #       PD Control: Time Design Strategy
        ####################################################
        # tuning parameters
        tr = 0.08          # Rise time for inner loop (theta)
        zeta = 0.707        # closed loop Damping Coefficient
        w_n = 2.2 / tr
        
        self.kd = 2 * zeta * w_n * (P.R * P.m * (P.radius ** 2)) / (2 * P.kt + 2 *(P.kt ** 2))
        self.kp = w_n**2 * (P.R * P.m * (P.radius ** 2)) / (2 * P.kt)

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