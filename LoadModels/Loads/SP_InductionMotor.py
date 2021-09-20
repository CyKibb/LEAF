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
        return lambda states, t, V, f: self.getNextState(states, t, V, f)

    def __getLoadTorque(self, wm):
        return 0 #self.Tnom*(self.A*((wm)**2))

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

    def __LoadIntegrator(self, t, x0, V, f):
        return odeint(self.getNextStateWrapper, x0, t, args=(V, f))

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
    def getNextState(self, states, t, v, f):
        i_windings = self.__getWindingCurrents(states)
        Tmech = self.__getMechTorque(states[4], i_windings)
        Tload = Tmech #self.__getLoadTorque(states[5])
        dlambda_maindt = v[0] - i_windings[0][0] * self.rmain
        dlambda_auxdt = v[1] - i_windings[1][0] * self.raux
        dlambda_r1dt = -1 * i_windings[2][0] * self.rr
        dlambda_r2dt = -1 * i_windings[3][0] * self.rr
        dthetadt = states[4]
        dwmdt = (1/self.J)*(Tmech - 1*Tload)
        # print("theta:", states[4] % (2*np.pi))
        # print("Rotor Angular Velocity:", states[5])
        return [dlambda_maindt, dlambda_auxdt, dlambda_r1dt, dlambda_r2dt, dthetadt, dwmdt]

    def getLoadPower(self, V, we, ts):
        # Integrate the states to solve
        states = self.__LoadIntegrator(ts, self.x0, V, we)
        # Adjust States for the next pass on interval
        self.x0 = states[1].tolist()
        print("self.xo:", self.x0)
        return states.tolist()

    # def UnitTest_getLoadPower(self, V, we, ts, theta):
    #     # This for loop should only be needed for the unit test simulation
    #     currentreturn = []
    #     response = []
    #     for i in range(len(ts) - 1):
    #         # Time Step to Integrate Over
    #         t = [ts[i], ts[i + 1]]
    #         # Calculate the Rotor Slip Coefficient
    #         slip = (we-self.x0[4])/we
    #         # Determine the mechanical speed of the rotor
    #         wm = ((1-slip)*we)
    #         # Calculate the Instantaneous Rotor Angle (double check ts[index]
    #         theta_me = self.wm*ts[0]
    #         # Calculate Winding Currents
    #         i_windings = self.__getWindingCurrents(self.x0, theta_me)
    #         # Find the Mechanical & Load Torque
    #         Tmech = self.__getMechTorque(theta_me, i_windings)
    #         Tload = self.__getLoadTorque(wm)
    #         # Integrate the States (find the flux linkages)
    #         states = self.__LoadIntegrator(t, self.x0, V, i_windings, we, theta_me, Tmech, Tload)
    #         # Adjust States for the next pass on interval
    #         self.x0 = states[1].tolist()
    #         # Append the currents and voltages to a list so that we can calculate active and reactive power
    #         response.append(self.x0)
    #         currentreturn.append(i_windings)
    #
    #     return




# def TwoPhase_InductionMotorModel(theta_me, fluxlinkages):
#     lmain = 0.0806       # Self-inductance of the main winding
#     laux = 0.196        # Self-inductance of the auxiliary winding
#     lr = 0.0000047          # Self-inductance of the equivalent rotor winding
#     lmainr = 0.000588      # Mutual inductance of the main and rotor windings
#     lauxr = 0.000909       # Mutual inductance of the auxiliary and rotor windings
#
#     # Lambda_vec = Machine_Inductance_Matrix * Current_vec
#
#     mi_matrix = np.array(
#         [[lmain, 0, lmainr * np.cos(theta_me), -1 * lmainr * np.sin(theta_me)],
#          [0, laux, -1 * lauxr * np.sin(theta_me), -1 * lauxr * np.cos(theta_me)],
#          [lmain * np.cos(theta_me), lauxr * np.sin(theta_me), lr, 0],
#          [-1 * lmain * np.sin(theta_me), -1 * lauxr * np.cos(theta_me), 0, lr]]
#     )
#     print(mi_matrix.shape)
#     print(fluxlinkages.shape)
#     # Solve for the currents in the windings
#     currents = np.linalg.solve(mi_matrix, fluxlinkages)
#     print("Currents:", currents)



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
        [0,0,0,0,3.14,50],
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

def singlephase_dq0():
    # Define Number of Sample Pointer required
    N = 10000
    # Simulation Total Time (s)
    T_tot = 5
    # Define Time Row Vector to Use
    ts = np.linspace(0.0, T_tot, N)
    # Bus frequency
    welec = 377  # rad/s
    theta_0 = 0  # radians
    theta_elec = welec * ts
    theta_main = welec * ts + (0)

    Vmain = 240*np.cos(theta_main)
    # Transform to alpha beta frame first
    Valpha = Vmain
    Vbeta = 240*np.cos(theta_main+1.5708)

    Vd = Valpha*np.cos(theta_elec) -1*Vbeta*np.sin(theta_elec)
    Vq = -1*Valpha*np.sin(theta_elec) -1*Vbeta*np.cos(theta_elec)
    LVNetworkPlotter.plotSingleBus(ts, Valpha)
    LVNetworkPlotter.plotSingleBus(ts, Vbeta, True)
    LVNetworkPlotter.plotSingleBus(ts, Vd)
    LVNetworkPlotter.plotSingleBus(ts, Vq, True)

    Vaux = 240*np.cos(theta_elec + 1.5708)

    dr = np.cos(theta_elec) -1*np.sin(theta_elec)
    qr = -1*np.sin(theta_elec) -1*np.cos(theta_elec)

    # LVNetworkPlotter.plotSingleBus(ts, Vmain)
    # LVNetworkPlotter.plotSingleBus(ts, Vaux, True)
    # LVNetworkPlotter.plotSingleBus(ts, vdr)
    # LVNetworkPlotter.plotSingleBus(ts, vqr, True)


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
