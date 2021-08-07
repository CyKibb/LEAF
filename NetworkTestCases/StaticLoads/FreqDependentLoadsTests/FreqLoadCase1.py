# Internal Imports
from NetworkTestCases.StaticLoads.FreqDependentLoadsTests.NwkDefineFreqLoad1 import *
from NetworkPlotter.PowerNetworkPlotter import *
from NetworkModel.LowVoltageNetwork import *
# External Imports
import numpy as np


def simLVN_FreqLoadsCase1(ts):
    # Setup Low Voltage Network Simulation Env
    network = FreqCase1Define()
    # Setup Plotter to Display Results
    initialStates = network.getGenInitStates()
    plotter = LVNetworkPlotter
    results, frequency = network.SimulateNetwork(
        ts,
        initialStates[0],
        initialStates[1],
        2.8,
        LoadStep
    )
    # Display Results
    plotter.plotNetworkFrequency(ts, np.array(frequency))
    plotter.plotNetworkVoltages(ts, np.array(results[:, 4:8]))
    plotter.plotNetworkPhase(ts, np.sin(np.array(results[:, 0:3])))
    plotter.plotNetworkPhase(ts, np.array(results[:, 0:4]))
    plotter.plotMultiBusPhaseError(ts, np.array(results[:, 0:4]), np.array(results[:, 0]))
    pass


def LoadStep(network, t):
    if 3 <= t[0] < 3.5:
        # print("I executed Here")
        # ZIP Load Step at the individual Buses...
        network.Loads = [
            FreqDependentLoad(
                1.0,
                -1.7,
                377,
                ExponentialLoad(
                    P0=1.4,
                    Q0=0.2,
                    V0=1.0,
                    np=0.72,
                    nq=2.96
                ),
            ),
            FreqDependentLoad(
                1.0,
                -1.7,
                377,
                ExponentialLoad(
                    P0=1.4,
                    Q0=0.2,
                    V0=1.0,
                    np=0.72,
                    nq=2.96
                ),
            ),
            FreqDependentLoad(
                1.0,
                -1.7,
                377,
                ExponentialLoad(
                    P0=1.4,
                    Q0=0.2,
                    V0=1.0,
                    np=0.72,
                    nq=2.96
                ),
            ),
            FreqDependentLoad(
                1.0,
                -1.7,
                377,
                ExponentialLoad(
                    P0=1.4,
                    Q0=0.2,
                    V0=1.0,
                    np=0.72,
                    nq=2.96
                ),
            ),
        ]
    # else:
    #     # Define Network Coupling Admittances
    #     yb12 = yb21 = np.complex(33333, 27824.15)
    #     yb14 = yb41 = np.complex(33333, 27824.15)
    #     yb34 = yb43 = np.complex(33333, 27824.15)
    #     yb23 = yb32 = np.complex(33333, 27824.15)
    #     yb13 = yb24 = yb31 = yb42 = 0  # np.complex(333, 274.15)
    #     # Define Driving Point Admittances (EXCEPT SHUNT LOAD ADMITTANCE)
    #     yb11 = np.complex(0, 0) + yb12 + yb14
    #     yb22 = np.complex(0, 0) + yb21 + yb23
    #     yb33 = np.complex(0, 0) + yb32 + yb34
    #     yb44 = np.complex(0, 0) + yb41 + yb43
    #     # Define Final Network Coupling Matrix
    #     network.Y = np.array(
    #         [[yb11, yb12, yb13, yb14],
    #          [yb21, yb22, yb23, yb24],
    #          [yb31, yb32, yb33, yb34],
    #          [yb41, yb42, yb43, yb44]]
    #     )
    pass