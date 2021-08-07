# Internal Imports
from NetworkTestCases.StaticLoads.ZIPLoadTests.NwkDefineZIPLoad1 import *
from NetworkPlotter.PowerNetworkPlotter import *
from NetworkModel.LowVoltageNetwork import *
# External Imports
import numpy as np


def simLVN_ZIPLoadsCase2(ts):
    # Setup Low Voltage Network Simulation Env
    network = ZIPCase1Define()
    # Setup Plotter to Display Results
    plotter = LVNetworkPlotter
    results, frequency = network.SimulateNetwork(
        ts,
        network.getGenInitStates(),
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
            ZIPpolynomialLoad(
                0.6,
                0.2,
                1.0,
                1.6,
                -2.69,
                2.09,
                12.53,
                -21.1,
                9.58
            ),
            ZIPpolynomialLoad(
                0.9,
                0.1,
                1.0,
                3.0,
                -2.69,
                2.09,
                12.53,
                -21.1,
                9.58
            ),
            ZIPpolynomialLoad(
                1.3,
                0.3,
                1.0,
                1.0,
                -2.69,
                2.09,
                12.53,
                -21.1,
                9.58
            ),
            ZIPpolynomialLoad(
                1.8,
                0.5,
                1.0,
                5.0,
                -2.69,
                2.09,
                12.53,
                -21.1,
                9.58
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