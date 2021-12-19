import numpy as np

from GenerationModels.InverterModel import SinglePhaseInverter
from LoadModels.DynamicLoads import ExponentialRecoveryLoad
from LoadModels.StaticLoads import ZIPpolynomialLoad, FreqDependentLoad, ExponentialLoad, EPRILoadsyn

'''
    This file defines the loads and generation on each bus with its own class. 
    The Bus class uses composition to compose a load and generation under simulation.
'''


class Bus0:

    def __init__(self):
        self.generation = SinglePhaseInverter(
            ID=1,
            ni=62.5,
            mi=2.143,
            Ke=10,
            tao=10.0,
            Prated=0.1,
            wn=377,
            Ei=1.0,
            init_Phase=0.0,
            E0=1.0,
            f0=377
        )
        self.initLoad = EPRILoadsyn(
                V0=1.0,
                f0=377,
                S0=(0.05, 0.0136),
                Sfrac=(1.0, 1.0),
                Ki=(0, 0),
                Kc=(0, 0),
                K1=(0.2, 0.4845),
                K2=(0.5, 0.672),
                kf1=(1.0, -2.8),
                kf2=(1.9, 1.2),
                nv1=(1.0, 3.0),
                nv2=(0.1, 0.5)
            )
        self.loadStep = ExponentialRecoveryLoad(
            T=(127.6, 75.3),
            init_x=[0.08, 0.02],
            S0=(0.08, 0.02),
            V0=(1.0),
            alphaT=(2.26, 5.22),
            alphaS=(0.38, 2.68)
        )


class Bus1:

    def __init__(self):
        self.generation = SinglePhaseInverter(
            ID=2,
            ni=41.67,
            mi=1.429,
            Ke=10,
            tao=5.0,
            Prated=0.15,
            wn=377,
            Ei=1.0,
            init_Phase=0.0,
            E0=1.0,
            f0=377
        )
        self.initLoad = EPRILoadsyn(
                V0=1.0,
                f0=377,
                S0=(0.10, 0.0254),
                Sfrac=(1.0, 1.0),
                Ki=(0, 0),
                Kc=(0, 0),
                K1=(0.2, 0.4845),
                K2=(0.5, 0.672),
                kf1=(1.0, -2.8),
                kf2=(1.9, 1.2),
                nv1=(1.0, 3.0),
                nv2=(0.1, 0.5)
            )
        self.loadStep = ExponentialRecoveryLoad(
            T=(127.6, 75.3),
            init_x=[0.1, 0.03],
            S0=(0.1, 0.03),
            V0=(1.0),
            alphaT=(2.26, 5.22),
            alphaS=(0.38, 2.68)
        )


class Bus2:

    def __init__(self):
        self.generation = SinglePhaseInverter(
            ID=3,
            ni=56.818,
            mi=1.948,
            Ke=10,
            tao=5.0,
            Prated=0.11,
            wn=377,
            Ei=1.0,
            init_Phase=0.0,
            E0=1.0,
            f0=377
        )
        self.initLoad = EPRILoadsyn(
                V0=1.0,
                f0=377,
                S0=(0.05, 0.0136),
                Sfrac=(1.0, 1.0),
                Ki=(0, 0),
                Kc=(0, 0),
                K1=(0.2, 0.4845),
                K2=(0.5, 0.672),
                kf1=(1.0, -2.8),
                kf2=(1.9, 1.2),
                nv1=(1.0, 3.0),
                nv2=(0.1, 0.5)
            )
        self.loadStep = ExponentialRecoveryLoad(
            T=(127.6, 75.3),
            init_x=[0.08, 0.03],
            S0=(0.08, 0.03),
            V0=(1.0),
            alphaT=(2.26, 5.22),
            alphaS=(0.38, 2.68)
        )


class Bus3:

    def __init__(self):
        self.generation = SinglePhaseInverter(
            ID=4,
            ni=31.21,
            mi=1.071,
            Ke=10,
            tao=10.0,
            Prated=0.2,
            wn=377,
            Ei=1.0,
            init_Phase=0.0,
            E0=1.0,
            f0=377
        )
        self.initLoad = EPRILoadsyn(
                V0=1.0,
                f0=377,
                S0=(0.1, 0.0372),
                Sfrac=(1.0, 1.0),
                Ki=(0, 0),
                Kc=(0, 0),
                K1=(0.2, 0.4845),
                K2=(0.5, 0.672),
                kf1=(1.0, -2.8),
                kf2=(1.9, 1.2),
                nv1=(1.0, 3.0),
                nv2=(0.1, 0.5)
            )
        self.loadStep = ExponentialRecoveryLoad(
            T=(127.6, 75.3),
            init_x=[0.105, 0.0272],
            S0=(0.105, 0.0272),
            V0=(1.0),
            alphaT=(2.26, 5.22),
            alphaS=(0.38, 2.68)
        )

# TODO: Add Network Fault Handling
class Network:
    # Define Static Loads (Shunt Admittances)
    # Y1 = np.complex(0.4, 0.44)
    # Y2 = np.complex(0.24, 0.132)
    # Y3 = np.complex(0.48, 0.264)
    # Y4 = np.complex(0.8, 0.22)
    # Define Network Coupling Admittances
    yb12 = yb21 = np.complex(4.957, 1.313)
    yb14 = yb41 = np.complex(4.957, 1.313)
    yb34 = yb43 = np.complex(4.957, 1.313)
    yb23 = yb32 = np.complex(4.957, 1.313)
    yb13 = yb24 = yb31 = yb42 = np.complex(4.957, 1.313)
    # Define Driving Point Admittances (EXCEPT SHUNT LOAD ADMITTANCE)
    yb11 = yb12 + yb14 + yb13
    yb22 = yb21 + yb23 + yb24
    yb33 = yb32 + yb34 + yb31
    yb44 = yb41 + yb43 + yb42

    # Yb11 = L1 + Yb12 + Yb14
    # Yb22 = L2 + Yb21 + Yb23
    # Yb33 = L3 + Yb32 + Yb34
    # Yb44 = L4 + Yb41 + Yb43

    def __init__(self):
        self.Y = np.array(
            [[self.yb11, self.yb12, self.yb13, self.yb14],
             [self.yb21, self.yb22, self.yb23, self.yb24],
             [self.yb31, self.yb32, self.yb33, self.yb34],
             [self.yb41, self.yb42, self.yb43, self.yb44]]
        )

    def NetworkFault(self,):
        return
