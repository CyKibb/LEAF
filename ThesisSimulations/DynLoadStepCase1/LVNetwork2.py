# Internal Imports
from LoadModels.DynamicLoads import ExponentialRecoveryLoad
from LoadModels.StaticLoads import ZIPpolynomialLoad, FreqDependentLoad, ExponentialLoad
from GenerationModels.InverterModel import SinglePhaseInverter
from NetworkModel.LowVoltageNetwork import LowVoltageNetwork
# External Imports
import numpy as np


# TODO: The types of loads we use in the simulation should be well defined for the type of network we are working in

def LVNetwork1Case2Define():
    # Note: Loads are Exponential-Frequency Dependent Loads (Summer Residential)
    network = LowVoltageNetwork(
        4,
        50000,
        240,
        [
            SinglePhaseInverter(
                1,
                62.5,
                2.143,
                1.0,
                5.0,
                0.1,
                377,
                1.0,
                0.0,
                1.0,
                377
            ),
            SinglePhaseInverter(
                2,
                41.67,
                1.429,
                1.0,
                5.0,
                0.15,
                377,
                1.0,
                0.0,
                1.0,
                377
            ),
            SinglePhaseInverter(
                3,
                56.818,
                1.948,
                1.0,
                5.0,
                0.11,
                377,
                1.0,
                0.0,
                1.0,
                377
            ),
            SinglePhaseInverter(
                4,
                31.21,
                1.071,
                1.0,
                5.0,
                0.2,
                377,
                1.0,
                0.0,
                1.0,
                377
            )],
       [
        ExponentialRecoveryLoad(
            (127.6, 75.3),
            [0.2, 0.03],
            (0.2, 0.03),
            (1.0),
            (2.26, 5.22),
            (0.38, 2.68)
        ),
        ExponentialRecoveryLoad(
            (127.6, 75.3),
            [0.15, 0.04],
            (0.15, 0.04),
            (1.0),
            (2.26, 5.22),
            (0.38, 2.68)
        ),
        ExponentialRecoveryLoad(
            (127.6, 75.3),
            [0.1, 0.07],
            (0.1, 0.07),
            (1.0),
            (2.26, 5.22),
            (0.38, 2.68)
        ),
        ExponentialRecoveryLoad(
            (127.6, 75.3),
            [0.12, 0.02],
            (0.12, 0.02),
            (1.0),
            (2.26, 5.22),
            (0.38, 2.68)
        )
    ]
    )
    NWKCoupling(network)
    return network


def NWKCoupling(network):
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
    # Define Final Network Coupling Matrix
    network.Y = np.array(
        [[yb11, yb12, yb13, yb14],
         [yb21, yb22, yb23, yb24],
         [yb31, yb32, yb33, yb34],
         [yb41, yb42, yb43, yb44]]
    )
