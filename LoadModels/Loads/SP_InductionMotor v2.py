from LoadModels.StaticLoads import ExponentialLoad
from scipy.integrate.odepack import odeint
import numpy as np
from NetworkPlotter.PowerNetworkPlotter import *

# Unit test file for a single-phase induction motor
'''
    Note: Induction Motor Model is Obtained from:
    Final Project Report: Load Modelling Transmission Research Berkley Lab
    Richard Bravo et al.
    Appendix d Pg 285....
'''

class SinglePhaseInductionMotor:

    def __init__(self, vbase, pbase, init_x0, lmain, laux, lr, lmainr, lauxr, rmain, raux, rr, J, Pmechloss, poles_num, A, B, C):
        # Base powers...
        self.vbase = vbase
        self.pbase = pbase
        # Machine Inductances
        self.lmain = lmain          # Self-inductance of the main winding
        self.laux = laux            # Self-inductance of the auxiliary winding
        self.lr = lr                # Self-inductance of the equivalent rotor winding
        self.lmainr = lmainr        # Mutual inductance of the main and rotor windings
        self.lauxr = lauxr          # Mutual inductance of the auxiliary and rotor windings
        # Machine Resistances
        self.rmain = rmain
        self.raux = raux
        self.rr = rr
        # Machine Inertial Constant
        self.J = J
        # Mechanical Losses
        self.Pmechloss = Pmechloss
        self.poles_num = poles_num
        # Initial State
        self.x0 = init_x0
        self.__x0
        # Mechanical Load Properties
        self.A = 1
        # self.wm
        self.wr = []
        self.Tnom = 1

    @property
    def x0(self):
        return self.__x0

    @x0.setter
    def x0(self, val):
        # if not isinstance(val, list):
        #     raise TypeError("x0 is a mandatory list object, please address...")
        self.__x0 = val

    @property
    def getNextStateWrapper(self):
        return lambda states, t, V, f, i, Tmech, Tload: self.getNextState(states, t, V, f, i, Tmech, Tload)

    def __getLoadTorque(self, wm):
        return (self.A*((wm)**2)) #self.Tnom*...

    def __getWindingCurrents(self, states):
        fluxlinkages = np.array(states[:4]).reshape((4, 1))
        mi_matrix = np.array(
            [[self.lmain, 0, self.lmainr * np.cos(states[4]), -1 * self.lmainr * np.sin(states[4])],
             [0, self.laux, 1 * self.lauxr * np.sin(states[4]), 1 * self.lauxr * np.cos(states[4])],
             [self.lmain * np.cos(states[4]), self.lauxr * np.sin(states[4]), self.lr, 0],
             [-1 * self.lmain * np.sin(states[4]), 1 * self.lauxr * np.cos(states[4]), 0, self.lr]]
        )
        # print("flux linkages:", fluxlinkages)
        # print("mi_matrix shape;", mi_matrix.shape)
        # print("mi_matrix:", mi_matrix)
        # print("Solved Currents:", np.linalg.solve(mi_matrix, fluxlinkages))
        return np.linalg.solve(mi_matrix, fluxlinkages)

    def __getMechTorque(self, theta_me, i):
        Tmech = (self.poles_num / 2) * (
                (-1 * self.lmainr * ((i[0][0] * i[2][0] * np.sin(theta_me)) + (i[0][0] * i[3][0])*np.cos(theta_me))) +
                (self.lauxr * ((i[1][0] * i[2][0] * np.cos(theta_me)) - (i[1][0] * i[3][0] * np.sin(theta_me))))
        )
        # print("Tmech:", Tmech)
        return Tmech

    def __LoadIntegrator(self, t, x0, V, f, i, Tmech, Tload):
        return odeint(self.getNextStateWrapper, x0, t, args=(V, f, i, Tmech, Tload))

    """ States to be passed in are:
        - Lambda_main
        - Lambda_aux
        - Lambda_r1
        - Lambda_r2
        States Order: states = [Lambda_main, Lambda_aux, Lambda_r1, Lambda_r2, wm]
        Passed in values: 
        - v = [vmain, vaux]
        - i = [imain, iaux, ir1, ir2]
    """
    def getNextState(self, states, t, v, f, i_windings, Tmech, Tload):

        dlambda_maindt = v[0] - i_windings[0][0] * self.rmain
        dlambda_auxdt = v[1] - i_windings[1][0] * self.raux
        dlambda_r1dt = -1 * i_windings[2][0] * self.rr
        dlambda_r2dt = -1 * i_windings[3][0] * self.rr
        dthetadt = states[4]
        dwmdt = (1/self.J)*(Tmech - 1*Tload)
        return [dlambda_maindt, dlambda_auxdt, dlambda_r1dt, dlambda_r2dt, dthetadt, dwmdt]

    def getLoadPower(self, V, we, ts):
        # Integrate the states to solve
        i = self.__getWindingCurrents(self.x0)
        Tmech = self.__getMechTorque(self.x0[4], i)
        Tload = self.__getLoadTorque(self.x0[5])
        states = self.__LoadIntegrator(ts, self.x0, V, we, i, Tmech, Tload)
        # Adjust States for the next pass on interval
        self.x0 = states[1].tolist()
        print("self.xo:", self.x0)
        return states.tolist()



def unittest():
    # Define Number of Sample Pointer required
    N = 10000
    # Simulation Total Time (s)
    T_tot = 10000
    # Define Time Row Vector to Use
    ts = np.linspace(0.0, T_tot, N)
    # Bus frequency
    welec = 377 # rad/s
    theta_0 = 0 #radians
    theta_me = welec*ts + theta_0

    Vmain = 240*np.cos(welec*ts)
    Vaux = 240*np.cos(welec*ts - (np.pi/2))

    Motor = SinglePhaseInductionMotor(
        1,
        1,
        [0.005,0.005,0.005,0.005,3.14,50],
        lmain=0.0806,
        laux=0.196,
        lr=0.0000047,
        lmainr=0.000588,
        lauxr=0.000909,
        rmain=0.58,
        rr=3.37,
        raux=0.0000376,
        J = 10,
        Pmechloss=1,
        poles_num=2,
        A=2,
        B=None,
        C=None
    )
    dxdt = []
    dxdt.append(Motor.x0)
    # Loop through to calculate next states...
    for i in range(len(ts) - 1):
        print(Vbus[:,i])
        t = [ts[i], ts[i + 1]]
        x = Motor.getLoadPower(
            Vbus[:,i],
            377,
            t
        )
        print("return vals:", x)

if __name__ == '__main__':
    # Define Number of Sample Pointer required
    N = 10000
    # Simulation Total Time (s)
    T_tot = 5
    # Define Time Row Vector to Use
    ts = np.linspace(0.0, T_tot, N)

    welec = 377  # rad/s
    Vmain = 240*np.cos(welec*ts)
    Vaux = -1*240*np.sin(welec*ts)
    Vbus = np.array((Vmain, Vaux))
    # print(Vbus)
    # print("Vbus", Vbus[:,1])
    # print("Vbus Shape:", Vbus.shape)
    unittest()
    # singlephase_dq0()
    # unittest()
