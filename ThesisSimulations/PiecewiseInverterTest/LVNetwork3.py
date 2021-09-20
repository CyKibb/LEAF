# Internal Imports
from LoadModels.StaticLoads import ZIPpolynomialLoad, FreqDependentLoad, ExponentialLoad
from GenerationModels.InverterModel import SinglePhaseInverter, SPInverterPieceWise
from NetworkModel.LowVoltageNetwork import LowVoltageNetwork
# External Imports
import numpy as np


# TODO: The types of loads we use in the simulation should be well defined for the type of network we are working in

def LVNetwork3Case3Define():
    # Note: Loads are Exponential-Frequency Dependent Loads (Summer Residential)
    network = LowVoltageNetwork(
        4,
        50000,
        240,
        [
            SPInverterPieceWise(
                ID=1,
                ni=(62.5, 62.5),
                mi=(2.143, 10.0),
                Ke=1.0,
                tao=5.0,
                Prated=0.1,
                wn=377,
                Ei=1.0,
                init_Phase=0.0,
                E0=1.0,
                f0=377
            ),
            SPInverterPieceWise(
                ID=2,
                ni=(41.67, 41.67),
                mi=(1.429, 6.7),
                Ke=1.0,
                tao=5.0,
                Prated=0.15,
                wn=377,
                Ei=1.0,
                init_Phase=0.0,
                E0=1.0,
                f0=377
            ),
            SPInverterPieceWise(
                ID=3,
                ni=(56.818, 56.818),
                mi=(1.948, 9.1),
                Ke=1.0,
                tao=5.0,
                Prated=0.11,
                wn=377,
                Ei=1.0,
                init_Phase=0.0,
                E0=1.0,
                f0=377
            ),
            SPInverterPieceWise(
                ID=4,
                ni=(31.21, 31.21),
                mi=(1.071, 5.0),
                Ke=1.0,
                tao=5.0,
                Prated=0.2,
                wn=377,
                Ei=1.0,
                init_Phase=0.0,
                E0=1.0,
                f0=377
            )],
        [
            FreqDependentLoad(
                0.7,
                -2.3,
                377,
                ExponentialLoad(
                    P0=0.09,
                    Q0=0.0436,
                    V0=1.0,
                    np=1.2,
                    nq=2.7
                )
            ),
            FreqDependentLoad(
                0.7,
                -2.3,
                377,
                ExponentialLoad(
                    P0=0.135,
                    Q0=0.0654,
                    V0=1.0,
                    np=1.2,
                    nq=2.7
                )
            ),
            FreqDependentLoad(
                0.7,
                -2.3,
                377,
                ExponentialLoad(
                    P0=0.09,
                    Q0=0.0436,
                    V0=1.0,
                    np=1.2,
                    nq=2.7
                )
            ),
            FreqDependentLoad(
                0.7,
                -2.3,
                377,
                ExponentialLoad(
                    P0=0.2,
                    Q0=0.0872,
                    V0=1.0,
                    np=1.2,
                    nq=2.7
                )
            ),
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
