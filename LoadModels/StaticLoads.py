import numpy as np


class ZIPpolynomialLoad:
    """ --------------------
    docstring for Polynomial ZIP Model
    -------------------------"""

    # Polynomial ZIP Model Constructor
    def __init__(self, P0, Q0, V0, a1, a2, a3, a4, a5, a6):
        # Polynomial ZIP Model Intial Conditions (Public)
        self.P0 = P0
        self.Q0 = Q0
        self.V0 = V0
        # Polynomial ZIP Model Coefficients (Private)
        self.__a1 = a1
        self.__a2 = a2
        self.__a3 = a3
        self.__a4 = a4
        self.__a5 = a5
        self.__a6 = a6

    def getLoadPower(self, V, f):
        # Note: We need to pay attenetion with the initial coniditions as well as
        # passing in an array or not...
        PL = self.P0 * (self.__a1 * (V / self.V0) ** 2 + self.__a2 * (V / self.V0) + self.__a3)
        QL = self.Q0 * (self.__a4 * (V / self.V0) ** 2 + self.__a5 * (V / self.V0) + self.__a6)
        return PL, QL

    def ZIP_UnitTest(self, V):
        return self.getLoadPower(V)


class ExponentialLoad:
    """ --------------------
    docstring for Polynomial ZIP Model
    -------------------------"""

    # Polynomial ZIP Model Constructor
    def __init__(self, P0, Q0, V0, np, nq):
        # Polynomial ZIP Model Intial Conditions (Public)
        self.P0 = P0
        self.Q0 = Q0
        self.V0 = V0
        # Polynomial ZIP Model Coefficients (Private)
        self.np = np
        self.nq = nq

    def getLoadPower(self, V, f, ts):
        # Note: We need to pay attenetion with the initial coniditions as well as
        # passing in an array or not...
        PL = self.P0 * ((V / self.V0) ** self.np)
        QL = self.Q0 * ((V / self.V0) ** self.nq)
        return PL, QL

    def Exp_UnitTest(self, V):
        return self.getLoadPower(V)


class FreqDependentLoad:
    """ --------------------
    docstring for Frequency Dependent Load
    "
    This class is a *composition* USES AGGREGATION of the ZIP_Polynomial class
    and the Exponential class. We need to select which load model
    you would like to use during runtime.
    BaseLoad needs to be passed into the class as either Exponential or ZIP load...
    "
    -------------------------"""

    # FreqDependentLoad Model Constructor
    def __init__(self, kpf, kqf, f0, baseload=None):
        # Instantiate Base Load Models into frequency dependence
        self.__kpf = kpf
        self.__kqf = kqf
        self.__f0 = (f0/(2*np.pi))

        # Aggregate Base Load Models into frequency dependence
        self.BaseLoad = baseload
        # self.ZIPLoad = ZIPpolynomialLoad
        # self.ExpLoad = ExponentialLoad

    def getLoadPower(self, V, f, ts):
        SL = self.BaseLoad.getLoadPower(V, f, ts)
        # PL = SL[0] * (1 + self.__kpf * ((f - self.__f0) / self.__f0))
        # QL = SL[1] * (1 + self.__kpf * ((f - self.__f0) /
        PL = SL[0] * (1 + self.__kpf * ((f/(2*np.pi)) - self.__f0)) # According to the IEEE Load papers
        QL = SL[1] * (1 + self.__kpf * ((f/(2*np.pi)) - self.__f0))
        return PL, QL

    def Freq_Dependence(self, f):
        fp = (1 + self.__kpf * ((f - self.__f0) / self.__f0))
        fq = (1 + self.__kqf * ((f - self.__f0) / self.__f0))
        return fp, fq


class EPRILoadsyn:
    """ --------------------
    docstring for EPRI Load Syn Model
    EPRI loadsyn is an aggregation of different types of loads at a single bus...
    "
    This class uses the OOP principles of aggregation AND composition...

    The EPRI LoadSyn model serves as an extension of the static exponential load models
    and the frequency dependent models.

    In order to keep the class clean, we denoted the attribute 'Sx' to hold the real and reactive
    parameters as a tuple (Px,Qx).
    "
    -------------------------"""

    def __init__(self, V0, f0, S0, Sfrac,
                 Ki, Kc, K1, kf1, K2, kf2, nv1, nv2
                 ):
        # Super function added in the use case of multiple inheretence...
        super().__init__()

        # Initial EPRI Load settings by composing of Exponential classes
        self.Sz = ExponentialLoad(
            (1 - (Ki[0] + Kc[0] + K1[0] + K2[0])),
            (1 - (Ki[1] + Kc[1] + K1[1] + K2[1])),
            V0,
            2,
            2
        )  # Kpz, Kqz terms
        self.Si = ExponentialLoad(
            Ki[0], Ki[1],
            V0,
            1,
            1
        )  # Kpi, Kqi terms
        self.Sc = (Kc[0], Kc[1])  # Kpc, Kqc
        self.S1 = FreqDependentLoad(
            kf1[0],
            kf1[1],
            f0,
            ExponentialLoad(
                K1[0],
                K1[1],
                V0,
                nv1[0],
                nv1[1]
            )
        )  # Kp1, Kq1
        self.S2 = FreqDependentLoad(
            kf2[0],
            kf2[1],
            f0,
            ExponentialLoad(
                K2[0],
                K2[1],
                V0,
                nv2[0],
                nv2[1]
            )
        )  # Kp2, Kq2
        self.S0 = S0
        self.Sfrac = Sfrac

    def getLoadPower(self, V, f, ts):
        SLz = self.Sz.getLoadPower(V, f, ts)
        SLi = self.Si.getLoadPower(V, f, ts)
        SLc = self.Sc
        SLf1 = self.S1.getLoadPower(V, f, ts)
        SLf2 = self.S2.getLoadPower(V, f, ts)
        PL = SLz[0] + SLi[0] + SLc[0] + SLf1[0] + SLf2[0]
        QL = SLz[1] + SLi[1] + SLc[1] + SLf1[1] + SLf2[1]
        return (PL*(self.S0[0]*self.Sfrac[0])), (QL*(self.S0[1]*self.Sfrac[1]))


"""TODO: Add in a NULL Load bus """
