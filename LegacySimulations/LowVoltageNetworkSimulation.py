# Local Import Packages
from ast import Index
from numpy.lib.shape_base import tile
from LoadModels.StaticLoads import ZIPpolynomialLoad
from LoadModels.DynamicLoads import *
from NetworkModel.LowVoltageNetwork import LowVoltageNetwork
from GenerationModels.InverterModel import SinglePhaseInverter
from NetworkPlotter.PowerNetworkPlotter import LVNetworkPlotter

# External Import Packages
import numpy as np
from scipy.integrate.odepack import odeint
import matplotlib as mpl
import matplotlib.pyplot as plt


def DefineLVNetwork():
    Network = LowVoltageNetwork(
        4,
        15000,
        10000,
        [SinglePhaseInverter(
            86.36,
            0.5,
            1.0,
            10.0,
            0.5,
            377,
            1.0,
            0.23,
            0
        ),
            SinglePhaseInverter(
                143.94,
                0.833,
                10.0,
                10.0,
                0.3,
                377,
                1.0,
                0.5,
                0
            ),
            SinglePhaseInverter(
                71.97,
                0.4167,
                3.0,
                1.0,
                0.6,
                377,
                1.0,
                2.6,
                0
            ),
            SinglePhaseInverter(
                43.18,
                0.25,
                1.0,
                2.0,
                1.0,
                377,
                1.0,
                1.5,
                0
            )],
        [ZIPpolynomialLoad(
            0.1,
            0.1,
            1.0,
            1.6,
            -2.69,
            2.09,
            12.53,
            -21.1,
            9.58
        ),
            ZIPpolynomialLoad(
                0.1,
                0.1,
                1.0,
                1.6,
                -2.69,
                2.09,
                12.53,
                -21.1,
                9.58
            ),
            ZIPpolynomialLoad(
                1.0,
                0.1,
                1.0,
                1.6,
                -2.69,
                2.09,
                12.53,
                -21.1,
                9.58
            ),
            ZIPpolynomialLoad(
                1.4,
                0.1,
                1.0,
                1.6,
                -2.69,
                2.09,
                12.53,
                -21.1,
                9.58
            )]
    )

    # Define Static Loads
    L1 = np.complex(0.4, 0.44)
    L2 = np.complex(0.24, 0.132)
    L3 = np.complex(0.48, 0.264)
    L4 = np.complex(0.8, 0.22)
    # Define Network Coupling Admittances
    Yb12 = Yb21 = np.complex(33333, 27824.15)
    Yb14 = Yb41 = np.complex(33333, 27824.15)
    Yb34 = Yb43 = np.complex(33333, 27824.15)
    Yb23 = Yb32 = np.complex(33333, 27824.15)
    Yb13 = Yb24 = Yb31 = Yb42 = 0  # np.complex(333, 274.15)
    # Define Driving Point Admittances (EXCEPT SHUNT LOAD ADMITTANCE)
    Yb11 = np.complex(0, 0) + Yb12 + Yb14
    Yb22 = np.complex(0, 0) + Yb21 + Yb23
    Yb33 = np.complex(0, 0) + Yb32 + Yb34
    Yb44 = np.complex(0, 0) + Yb41 + Yb43
    # Yb11 = L1 + Yb12 + Yb14
    # Yb22 = L2 + Yb21 + Yb23
    # Yb33 = L3 + Yb32 + Yb34
    # Yb44 = L4 + Yb41 + Yb43
    # Define Final Network Coupling Matrix
    Network.Y = np.array(
        [[Yb11, Yb12, Yb13, Yb14],
         [Yb21, Yb22, Yb23, Yb24],
         [Yb31, Yb32, Yb33, Yb34],
         [Yb41, Yb42, Yb43, Yb44]]
    )
    return Network


def BusFault(Network, t):
    if t[0] >= 3 and t[0] < 3.5:
        # print("I executed Here")
        # Define Static Loads
        L1 = np.complex(0.4, 0.84)
        L2 = np.complex(0.7, 0.62)
        L3 = np.complex(0.48, 0.84)
        L4 = np.complex(0.8, 0.12)
        # Define Network Coupling Admittances
        Yb12 = Yb21 = np.complex(33333, 27824.15)
        Yb14 = Yb41 = np.complex(33333, 27824.15)
        Yb34 = Yb43 = np.complex(33333, 27824.15)
        Yb23 = Yb32 = np.complex(33333, 27824.15)
        Yb13 = Yb24 = Yb31 = Yb42 = 0  # np.complex(333, 274.15)
        # Define Driving Point Admittances (EXCEPT SHUNT LOAD ADMITTANCE)
        Yb11 = L1 + Yb12 + Yb14
        Yb22 = L2 + Yb21 + Yb23
        Yb33 = L3 + Yb32 + Yb34
        Yb44 = L4 + Yb41 + Yb43
        Network.Y = np.array(
            [[Yb11, Yb12, Yb13, Yb14],
             [Yb21, Yb22, Yb23, Yb24],
             [Yb31, Yb32, Yb33, Yb34],
             [Yb41, Yb42, Yb43, Yb44]]
        )
    else:
        # Define Network Coupling Admittances
        Yb12 = Yb21 = np.complex(33333, 27824.15)
        Yb14 = Yb41 = np.complex(33333, 27824.15)
        Yb34 = Yb43 = np.complex(33333, 27824.15)
        Yb23 = Yb32 = np.complex(33333, 27824.15)
        Yb13 = Yb24 = Yb31 = Yb42 = 0  # np.complex(333, 274.15)
        # Define Driving Point Admittances (EXCEPT SHUNT LOAD ADMITTANCE)
        Yb11 = np.complex(0, 0) + Yb12 + Yb14
        Yb22 = np.complex(0, 0) + Yb21 + Yb23
        Yb33 = np.complex(0, 0) + Yb32 + Yb34
        Yb44 = np.complex(0, 0) + Yb41 + Yb43
        # Define Final Network Coupling Matrix
        Network.Y = np.array(
            [[Yb11, Yb12, Yb13, Yb14],
             [Yb21, Yb22, Yb23, Yb24],
             [Yb31, Yb32, Yb33, Yb34],
             [Yb41, Yb42, Yb43, Yb44]]
        )


def NetworkUnitTest(Network, ts):
    Results, frequency = Network.SimulateNetwork(
        ts,
        Network.getGenInitStates(),
        0.5,
        BusFault
    )
    results = np.array(Results)
    # print(np.array(results[:,4:8]))
    plot = LVNetworkPlotter
    plot.plotNetworkFrequency(ts, np.array(frequency))
    plot.plotNetworkVoltages(ts, np.array(results[:, 4:8]))
    plot.plotNetworkPhase(ts, np.sin(np.array(results[:, 0:3])))
    plot.plotNetworkPhase(ts, np.array(results[:, 0:4]))
    # print("np.array(results[:,0:3])",np.array(results[:,0:3]))
    # print("np.array(results[:,0])", np.array(results[:,0]))
    plot.plotMultiBusPhaseError(ts, np.array(results[:, 0:4]), np.array(results[:, 0]))
    return


if __name__ == '__main__':
    # Define Number of Sample Pointer required
    N = 1000
    # # Simulation Total Time (s)
    T_tot = 5

    Network = DefineLVNetwork()
    print(Network.Generation[0].getInitStates())
    print(Network.getGenInitStates())
    # Run Network Unit Test
    NetworkUnitTest(
        DefineLVNetwork(),
        np.linspace(0.0, T_tot, N)
    )