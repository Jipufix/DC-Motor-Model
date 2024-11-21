import numpy as np
import DCParam as P

class ctrlPD:
    def __init__(self):
        ####################################################
        #       PD Control: Time Design Strategy
        ####################################################
        # tuning parameters
        tr_th = 0.15          # Rise time for inner loop (theta)
        M = 15.0              # Time scale separation 
        zeta = .707        # closed loop Damping Coefficient
        # saturation limits
        F_max = 5             		  # Max Force, N
        error_max = 1        		  # Max step size,m
        theta_max = 30.0 * np.pi / 180.0  # Max theta, rads
        #---------------------------------------------------
        #                    Inner Loop
        #---------------------------------------------------
        # parameters of the open loop transfer function
        #---------------------------------------------------
        #                    Outer Loop
        #---------------------------------------------------
        # coefficients for desired outer loop
        # print control gains to terminal        
        
        omega_n = 2.2 / zeta
        alpha_0 = omega_n**2
        alpha_1 = 2.0 * zeta * omega_n
        
        self.kd = 2 * zeta * omega_n * (P.R * P.m * (P.radius ** 2)) / (2 * (P.kt**2))
        self.kp = omega_n**2 * (P.R * P.m * (P.radius ** 2))
        #---------------------------------------------------
        #                    zero canceling filter
        #---------------------------------------------------

    def update(self, thetadot_r, state):
        theta = state[0][0]
        thetadot = state[1][0]
        thetaddot = state[2][0]

        V_tilde = self.kp * (thetadot_r - thetadot) - (self.kd * thetaddot)
        V_e = 0
        return saturate(V_tilde - V_e, P.VMax)
    
def saturate(u, limit):

    if abs(u) > limit:
        u = limit * np.sin(u)
    return u