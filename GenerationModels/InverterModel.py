import numpy as np


# Might need to inherent from IEEE15472018 class to determine it's properties
from scipy.integrate import odeint

from NetworkPlotter.PowerNetworkPlotter import LVNetworkPlotter


class SinglePhaseInverter:
    """ --------------------
    docstring for Single-Phase inverter generation source model
    ""
    Active power dynamics are in accordance with...
    ti*dEi/dt = Ke(Ei* - Ebk) - mi(Pi,nom - (PL,bk + Pbk,network))

    Reactive power dynamics are in accordance with...
    wi = wi* + ni(QL,bk + Qbk,network)

    Note:
    The dynamics and set points of the inverter should adhere to the
    IEEE 1547-2018 requirements

    -------------------------"""

    # SPInverter Constructor
    def __init__(self, ID, ni, mi, Ke, tao, Prated, wn, Ei, init_Phase, E0, f0,):
        self.InvID = ID
        # Droop Gain Set points
        self._ni = ni  # Rad/s/VAR
        self._mi = mi  # V/Watt
        self.Ke = Ke

        # Nominal Operation Set points
        self.wn = wn  # rad/s
        self.Ei = Ei  # V p.u.

        # Inverter Control Loop Delay Constant
        self.tao = tao

        # Inverter rated power
        self.Prated = Prated  # Rated active power injection
        self.Pnom = 0.8 * Prated  # Nominal active power injection set point
        self.QimaxInj = Prated * -0.44  # Max Reactive power injection
        self.QimaxAbs = Prated * 0.44  # Max Reactive power absorption

        # Initial States
        self.InitPhase = init_Phase
        self.E0 = E0
        self.f0 = f0
        # self.InitPhase = 2*np.pi()*np.random.random()

    # Droop Curve Functions.... (These should potentially be user defined not fixed?)
    def Inv_VW_DroopCurve(self):
        return lambda P: -1 * self._mi * (self.Pnom - P) + self.Ei

    def Inv_fVAR_DroopCurve(self):
        return lambda Q: self._ni * Q + self.wn

    def getInitStates(self):
        return self.InitPhase, self.E0, self.f0

    # Single-Phase Invester Dynamics
    ''' Note for usage within a network scenario Pout passed into must account
    for BOTH local and network loading at the buss the inverter is connected to.
    If not this function will need to be overridden.
    The vector for the ODE solver may be quite large on I am not sure whether 
    each differential should be solved individually.

    Each inverter may be assigned a column vector and therefore is required to 
    have a column Id to specify which column vector within the system matrix is 
    assigned to it?? 
    '''
#     TODO: Need to figure out how to limit power injection capabilities
# Todo: Handle the disconnect cases when P,Qout hits P,Qmax & min limits...
    def getNextState(self, x, t, Pout, Qout):
        #TODO: Evaluation of Pout + self.Pnom
        dEdt = (self.Ke) * (self.Ei - x[1]) - self._mi * (Pout + self.Pnom)  # Pi and Pnom might need to be switched...
        dthetadt = self.wn + self._ni * Qout
        return self.tao * dEdt, dthetadt

    def getNextStateWrapper(self):
        return lambda x, t, Pout, Qout: self.getNextState(x, t, Pout, Qout)



class SPInverterPieceWise(SinglePhaseInverter):

    def __init__(self, ID, ni, mi, Ke, tao, Prated, wn, Ei, init_Phase, E0, f0):
        # Check to ensure that we have received the correct inputs
        if not isinstance(ni, tuple):
            raise TypeError("ni is a mandatory tuple object, please address...")
        if not isinstance(mi, tuple):
            raise TypeError("mi is a mandatory tuple object, please address...")
        super().__init__(ID, ni, mi, Ke, tao, Prated, wn, Ei, init_Phase, E0, f0)

    def getNextState(self, x, t, Pout, Qout, ):
        # TODO: Add in the disconnect conditions in the extremities
        # Piece-Wise Linear Droop Curve V-W Curve
        # print("Pout",Pout)
        # print("Qout", Qout)
        dEdt = (self.Ke) * (self.Ei - x[1]) - self._mi[0] * (Pout - self.Pnom)  # Pi and Pnom might need to be switched...
        dthetadt = self.wn + self._ni[0] * Qout

        if Pout > self.Prated:
            dEdt = (self.Ke) * (self.Ei - x[1]) - self._mi[0] * (self.Prated - self.Pnom)
            # dEdt = 0
            # print('Pout >= self.Prated')
            # print("This is Pout",Pout, "THis is my ID", self.InvID, "This is my rating", self.Prated)
        elif Pout < self.Pnom:
            dEdt = (self.Ke) * (self.Ei - x[1]) - self._mi[0] * (
                    Pout + self.Pnom)  # Need to double check this information
            # print('Pout < self.Pnom')
            # print("This is Pout", Pout, "THis is my ID", self.InvID, "This is my rating", self.Prated)
        elif self.Pnom <= Pout <= self.Prated:
            dEdt = (self.Ke) * (self.Ei - x[1]) - self._mi[1] * (
                    Pout + self.Pnom)  # Need to double check this information
            # print('Pout >= self.Pnom and Pout <= self.Prated')
            # print("This is Pout", Pout, "THis is my ID", self.InvID, "This is my rating", self.Prated)
        elif 0.95 <= Pout <= 1.05:
            dEdt = (self.Ke) * (self.Ei - x[1]) - self._mi[0] * (self.Pnom)  # Need to double check this information
            # print('Pout >= 0.95 and Pout <= 1.05:')
            # print("This is Pout", Pout, "THis is my ID", self.InvID, "This is my rating", self.Prated)
        else:
            dEdt = (self.Ke) * (self.Ei - x[1]) - self._mi * (Pout + self.Pnom)

        # Piece-Wise Linear Droop Curve f-VAR Curve
        if 0 > Qout >= self.QimaxInj:
            dthetadt = self.wn + self._ni[0] * Qout
            # print('Qout < 0 and Qout >= self.QimaxInj:')
            # print("This is Qout:", Qout, "THis is my ID:", self.InvID, "This is my rating:", self.QimaxInj)
        elif Qout == 0:
            dthetadt = self.wn
            # print('Qout == 0:')
            # print("This is Qout:", Qout, "THis is my ID:", self.InvID, "This is my rating:", self.QimaxInj)
        elif 0 < Qout <= self.QimaxAbs:
            dthetadt = self.wn  + self._ni[1] * Qout
            # print('Qout > 0 and Qout <= self.QimaxAbs:')
            # print("This is Qout:", Qout, "THis is my ID:", self.InvID, "This is my rating:", self.QimaxAbs)
        elif Qout < self.QimaxInj:
            dthetadt = self.wn  + self._ni[1] * self.QimaxInj
            # print('Qout <= self.QimaxInj:')
            # print("This is Qout:", Qout, "THis is my ID:", self.InvID, "This is my rating:", self.QimaxInj)
        elif Qout > self.QimaxAbs:
            dthetadt = self.wn  + self._ni[1] * self.QimaxAbs
            # print('Qout >= self.QimaxAbs:')
            # print("This is Qout:", Qout, "THis is my ID:", self.InvID, "This is my rating:", self.QimaxAbs)
        else:
            dthetadt = self.wn + self._ni * Qout

        return self.tao * dEdt, dthetadt


def unittest():
    # Define Number of Sample Pointer required
    N = 100000
    # Simulation Total Time (s)
    T_tot = 4
    # Define Time Row Vector to Use
    ts = np.linspace(0.0, T_tot, N)
    # Define Unit Test Voltage Step
    Vbus = np.ones(N)
    # Create Unit Step Voltage Disturbance
    Vbus[int(N / 2):] *= 0.8
    # Define Pout
    Pout = np.ones(N)
    Qout = np.ones(N)
    Pout *= 0.5
    Qout *= 0.01
    print("Pout and Qout", Pout, Qout)
    # Define ERL Load Under Test
    inverter_test = SinglePhaseInverter(
        ID=1,
        ni=62.5,
        mi=2.143,
        Ke=1.0,
        tao=10.0,
        Prated=0.5,
        wn=377,
        Ei=0,
        init_Phase=0.6,
        E0=1.0,
        f0=377
    )
    # Loop through and test ERL state solver
    print("getInitStates test:", inverter_test.getInitStates()[:2])
    x = []
    PL = []
    x.append(inverter_test.getInitStates()[:2])
    x0 = inverter_test.getInitStates()[:2]

    # Loop through to calculate next states...
    for i in range(len(ts) - 1):
        t = [ts[i], ts[i + 1]]
        xode = odeint(inverter_test.getNextStateWrapper(), x0, t, args=(Pout[i], Qout[i]))
        xode[1, 0] = xode[1,0] % (2 * np.pi)
        x.append(xode[1])
        x0 = xode[1]
    x = np.array(x)
    # Next State and Load Power Vectors
    LVNetworkPlotter.plotSingleBus(ts, x[:,0], showplot=True)
    LVNetworkPlotter.plotSingleBus(ts, x[:,1], showplot=True)

if __name__ == '__main__':
    unittest()