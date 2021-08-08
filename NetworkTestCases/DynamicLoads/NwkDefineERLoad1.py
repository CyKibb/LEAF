# Internal Imports
from LoadModels.StaticLoads import EPRILoadsyn
from LoadModels.StaticLoads import ExponentialLoad
from LoadModels.StaticLoads import FreqDependentLoad
from LoadModels.DynamicLoads import ExponentialRecoveryLoad
from GenerationModels.InverterModel import SinglePhaseInverter
from NetworkModel.LowVoltageNetwork import LowVoltageNetwork

# External Imports
import numpy as np


# TODO: The types of loads we use in the simulation should be well defined for the type of network we are working in

def ERLCase1Define():
    network = LowVoltageNetwork(
        4,
        15000,
        10000,
        [
            SinglePhaseInverter(
                86.36,
                0.5,
                1.0,
                10.0,
                0.5,
                377,
                1.0,
                0.0,
                1.0,
                377
            ),
            SinglePhaseInverter(
                143.94,
                0.833,
                10.0,
                10.0,
                0.3,
                377,
                1.0,
                0.0,
                1.0,
                377
            ),
            SinglePhaseInverter(
                71.97,
                0.4167,
                3.0,
                1.0,
                0.6,
                377,
                1.0,
                0.0,
                1.0,
                377
            ),
            SinglePhaseInverter(
                43.18,
                0.25,
                1.0,
                2.0,
                1.0,
                377,
                1.0,
                0.0,
                1.0,
                377
            )],
        [
            EPRILoadsyn(
                1.0,
                377,
                (1.0, 1.0),
                (1.0, 1.0),
                (0.1, 0.1),
                (0.2, 0.2),
                (0.2, 0.485),
                (1.0, -2.8),
                (0.5, 0.672),
                (1.9, 1.2),
                (1.0, 3.0),
                (0.1, 0.5)
            ),
            EPRILoadsyn(
                1.0,
                377,
                (1.0, 1.0),
                (1.0, 1.0),
                (0.1, 0.1),
                (0.2, 0.2),
                (0.2, 0.485),
                (1.0, -2.8),
                (0.5, 0.672),
                (1.9, 1.2),
                (1.0, 3.0),
                (0.1, 0.5)
            ),
            EPRILoadsyn(
                1.0,
                377,
                (1.0, 1.0),
                (1.0, 1.0),
                (0.1, 0.1),
                (0.2, 0.2),
                (0.2, 0.485),
                (1.0, -2.8),
                (0.5, 0.672),
                (1.9, 1.2),
                (1.0, 3.0),
                (0.1, 0.5)
            ),
            EPRILoadsyn(
                1.0,
                377,
                (1.0, 1.0),
                (1.0, 1.0),
                (0.1, 0.1),
                (0.2, 0.2),
                (0.2, 0.485),
                (1.0, -2.8),
                (0.5, 0.672),
                (1.9, 1.2),
                (1.0, 3.0),
                (0.1, 0.5)
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
    yb12 = yb21 = np.complex(333, 278.15)
    yb14 = yb41 = np.complex(333, 278.15)
    yb34 = yb43 = np.complex(333, 278.15)
    yb23 = yb32 = np.complex(333, 278.15)
    yb13 = yb24 = yb31 = yb42 = 0  # np.complex(333, 274.15)
    # Define Driving Point Admittances (EXCEPT SHUNT LOAD ADMITTANCE)
    yb11 = yb12 + yb14
    yb22 = yb21 + yb23
    yb33 = yb32 + yb34
    yb44 = yb41 + yb43
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
