import numpy as np

from GenerationModels.InverterModel import SinglePhaseInverter, SPInverterPieceWise
from LoadModels.StaticLoads import ZIPpolynomialLoad, FreqDependentLoad, ExponentialLoad, EPRILoadsyn

'''
    This file defines the loads and generation on each bus with its own class. 
    The Bus class uses composition to compose a load and generation under simulation.
'''


class Bus0:

    def __init__(self):
        self.generation = SPInverterPieceWise(
            ID=1,
            ni=(62.5, 62.5),
            mi=(2.143, 10),
            Ke=0.0,
            tao=5.0,
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
        self.loadStep = EPRILoadsyn(
                V0=1.0,
                f0=377,
                S0=(0.09, 0.015),
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


class Bus1:

    def __init__(self):
        self.generation = SPInverterPieceWise(
            ID=2,
            ni=(41.67, 41.67),
            mi=(1.429, 6.667),
            Ke=0.0,
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
        self.loadStep = EPRILoadsyn(
                V0=1.0,
                f0=377,
                S0=(0.12, 0.03),
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


class Bus2:

    def __init__(self):
        self.generation = SPInverterPieceWise(
            ID=3,
            ni=(56.818, 56.818),
            mi=(1.948, 9.091),
            Ke=0.0,
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
        self.loadStep = EPRILoadsyn(
                V0=1.0,
                f0=377,
                S0=(0.01, 0.02),
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


class Bus3:

    def __init__(self):
        self.generation = SPInverterPieceWise(
            ID=4,
            ni=(31.21, 31.21),
            mi=(1.071, 5),
            Ke=0.0,
            tao=5.0,
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
        self.loadStep = EPRILoadsyn(
                V0=1.0,
                f0=377,
                S0=(0.14, 0.0001),
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


class NetworkCoupling:
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
