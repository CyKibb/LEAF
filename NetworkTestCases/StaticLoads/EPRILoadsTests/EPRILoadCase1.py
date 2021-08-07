# Internal Imports
from NetworkTestCases.StaticLoads.EPRILoadsTests.NwkDefineEPRILoad1 import *
from NetworkPlotter.PowerNetworkPlotter import *
from NetworkModel.LowVoltageNetwork import *
# External Imports
import numpy as np


def simLVN_EPRILoadsCase1(ts):
    # Setup Low Voltage Network Simulation Env
    network = EPRICase1Define()
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
                (0.6, 0.2),
                (0.2, 0.485),
                (1.0, -2.8),
                (0.1, 0.672),
                (1.9, 1.2),
                (1.0, 3.0),
                (0.1, 0.5)
            ),
            EPRILoadsyn(
                1.0,
                377,
                (1.0, 1.0),
                (1.0, 1.0),
                (0.4, 0.1),
                (0.2, 0.2),
                (0.2, 0.485),
                (1.0, -2.8),
                (0.2, 0.672),
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
                (0.1, 0.2),
                (0.1, 0.485),
                (1.0, -2.8),
                (0.7, 0.672),
                (1.9, 1.2),
                (1.0, 3.0),
                (0.1, 0.5)
            )
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