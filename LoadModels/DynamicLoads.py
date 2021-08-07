from LoadModels.StaticLoads import ExponentialLoad
from scipy.integrate.odepack import odeint
import numpy as np
from NetworkPlotter.PowerNetworkPlotter import *


# TODO: This class should be able to take what type of load model you would like to add to it.
class ExponentialRecoveryLoad:
    """ --------------------
    docstring for ERL dynamic load Model
    "
    Tpdxp/dt + xp = Ps(V) - Pt(V)
    Pl = xp + Pt(V)
    TqDxq/dt + xq = Qs(V) - Qt(V)
    Ql = xq + Qt(V)

    In order to keep the class clean, we denoted the attribute 'Sx' to hold the real and reactive
    parameters as a tuple (Px,Qx).
    Alpha = (alpha transient, alpha static)
    "
    -------------------------"""

    def __init__(self, T, init_x, S0, V0, alphaT, alphaS):
        self.Tp = T[0]
        self.Tq = T[1]
        self.Pt = ExponentialLoad(S0[0], S0[1], V0, alphaT[0], alphaT[1])
        self.Ps = ExponentialLoad(S0[0], S0[1], V0, alphaS[0], alphaS[1])
        self.x0 = init_x
        self.__x0

    @property
    def x0(self):
        return self.__x0

    @x0.setter
    def x0(self, val):
        if not isinstance(val, list):
            raise TypeError("x0 is a mandatory list object, please address...")
        self.__x0 = val

    @property
    def getNextStateWrapper(self):
        return lambda states, t, V, f: self.getNextState(states, t, V, f)

    def getNextState(self, states, t, V, f):
        SLexps = self.Ps.getLoadPower(V, f, t)
        SLexpt = self.Pt.getLoadPower(V, f, t)
        return (1 / (self.Tp)) * (SLexps[0] - SLexpt[0] - states[0]), (1 / (self.Tq)) * (
                    SLexps[1] - SLexpt[1] - states[1])

    def __LoadIntegrator(self, t, x0, V, f):
        return odeint(self.getNextStateWrapper, x0, t, args=(V, f))

    # All getLoadPowerAPI's need to have the format (V, f, t_int)
    def getLoadPower(self, V, f, ts):
        # print("Executing get Load Power for ERL load 0.0")
        # Integrate the state of the load...
        states = self.__LoadIntegrator(ts, self.x0, V, f)  # The return type is a list
        # Update the initial state for when the next api call happens within the simulation...
        self.x0 = states[1].tolist()
        # Get transient load power
        SLexp = self.Pt.getLoadPower(V, f, ts)
        # Return Load power
        return self.x0[0] + SLexp[0], self.x0[0] + SLexp[1]


def unittest():
    # Define Number of Sample Pointer required
    N = 10000
    # Simulation Total Time (s)
    T_tot = 10000
    # Define Time Row Vector to Use
    ts = np.linspace(0.0, T_tot, N)
    # Define Unit Test Voltage Step
    Vbus = np.ones(N)
    # Create Unit Step Voltage Disturbance
    Vbus[int(N / 2):] *= 0.8
    # Define ERL Load Under Test
    ERL_Load1 = ExponentialRecoveryLoad(
        (127.6, 75.3),
        [0.3, 1],
        (32.28, 5.56),
        (1.0),
        (2.26, 5.22),
        (0.38, 2.68)
    )
    # Loop through and test ERL state solver
    dxdt = []
    PL = []
    dxdt.append(ERL_Load1.x0)
    # Loop through to calculate next states...
    for i in range(len(ts) - 1):
        t = [ts[i], ts[i + 1]]
        x = ERL_Load1.getLoadPower(
            Vbus[i],
            0,
            t
        )
        dxdt.append(ERL_Load1.x0)
        PL.append(x)
    # Next State and Load Power Vectors
    dxdt = np.array(dxdt)
    PL = np.array(PL)
    print(PL)
    # Display Load Response Results
    LVNetworkPlotter.plotSingleBus(ts[1:], PL[:, 0])
    LVNetworkPlotter.plotSingleBus(ts[1:], PL[:, 1])


if __name__ == '__main__':
    unittest()
