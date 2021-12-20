import numpy as np

from GenerationModels.InverterModel import SinglePhaseInverter
from LoadModels.StaticLoads import ZIPpolynomialLoad, FreqDependentLoad, ExponentialLoad

'''
    This file defines the loads and generation on each bus with its own class. 
    The Bus class uses composition to compose a load and generation under simulation.
'''


class Bus0:

    def __init__(self):
        self.generation = SinglePhaseInverter(
            1,
            62.5,
            2.143,
            10.0,
            5.0,
            0.1,
            377,
            1.0,
            0.0,
            1.0,
            377
        )
        self.initLoad = FreqDependentLoad(
            0.7,
            -2.3,
            377,
            ExponentialLoad(
                P0=0.05,
                Q0=0.0136,
                V0=1.0,
                np=1.2,
                nq=2.7
            )
        )
        self.loadStep = FreqDependentLoad(
            0.7,
            -2.3,
            377,
            ExponentialLoad(
                P0=0.12,
                Q0=0.015,
                V0=1.0,
                np=1.2,
                nq=2.7
            )
        )


class Bus1:

    def __init__(self):
        self.generation = SinglePhaseInverter(
            2,
            41.67,
            1.429,
            10.0,
            5.0,
            0.15,
            377,
            1.0,
            0.0,
            1.0,
            377
        )
        self.initLoad = FreqDependentLoad(
            0.7,
            -2.3,
            377,
            ExponentialLoad(
                P0=0.1,
                Q0=0.0254,
                V0=1.0,
                np=1.2,
                nq=2.7
            )
        )
        self.loadStep = FreqDependentLoad(
            0.7,
            -2.3,
            377,
            ExponentialLoad(
                P0=0.12,
                Q0=0.03,
                V0=1.0,
                np=1.2,
                nq=2.7
            )
        )


class Bus2:

    def __init__(self):
        self.generation = SinglePhaseInverter(
            3,
            56.818,
            1.948,
            10.0,
            5.0,
            0.11,
            377,
            1.0,
            0.0,
            1.0,
            377
        )
        self.initLoad = FreqDependentLoad(
            0.7,
            -2.3,
            377,
            ExponentialLoad(
                P0=0.05,
                Q0=0.0136,
                V0=1.0,
                np=1.2,
                nq=2.7
            )
        )
        self.loadStep = FreqDependentLoad(
            0.7,
            -2.3,
            377,
            ExponentialLoad(
                P0=0.15,
                Q0=0.02,
                V0=1.0,
                np=1.2,
                nq=2.7
            )
        )


class Bus3:

    def __init__(self):
        self.generation = SinglePhaseInverter(
            4,
            31.21,
            1.071,
            10.0,
            5.0,
            0.2,
            377,
            1.0,
            0.0,
            1.0,
            377
        )
        self.initLoad = FreqDependentLoad(
            0.7,
            -2.3,
            377,
            ExponentialLoad(
                P0=0.1,
                Q0=0.0372,
                V0=1.0,
                np=1.2,
                nq=2.7
            )
        )
        self.loadStep = FreqDependentLoad(
            0.7,
            -2.3,
            377,
            ExponentialLoad(
                P0=0.105,
                Q0=0.0272,
                V0=1.0,
                np=1.2,
                nq=2.7
            )
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
