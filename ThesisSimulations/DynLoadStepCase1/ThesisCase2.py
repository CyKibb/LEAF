# Internal Imports
from LoadModels.DynamicLoads import ExponentialRecoveryLoad
from NetworkPlotter.PowerNetworkPlotter import *
# External Imports
import numpy as np

from ThesisSimulations.DynLoadStepCase1.LVNetwork2 import LVNetwork1Case2Define


def simLVN_ThesisCase2(ts):
    # Setup Low Voltage Network Simulation Env
    network = LVNetwork1Case2Define()
    # Setup Plotter to Display Results
    initialStates = network.getGenInitStates()
    plotter = LVNetworkPlotter
    results, frequency, Loads = network.SimulateNetwork(
        ts,
        initialStates[0],
        initialStates[1],
        2.8,
        returnloads=True
    )

    # Display Results
    plotter.plotNetworkFrequency(ts, np.array(frequency), showplot=True)
    plotter.plotMultiBusActivePower(ts, Loads[:,:,0], showplot=True)
    plotter.plotMultiBusReactivePower(ts, Loads[:,:,1], showplot=True)
    plotter.plotMultiBusPhaseError(ts, np.array(results[:, 0:4]), np.array(results[:, 0]), showplot=True)
    # plotter.plotNetworkVoltages(ts, np.array(results[:, 4:8]), showplot=True)
    # plotter.plotNetworkPhase(ts, np.sin(np.array(results[:, 0:3])), showplot=True)
    # plotter.plotNetworkPhase(ts, np.array(results[:, 0:4]), showplot=True)

    pass

def LoadStep(network, t):
    if 3 <= t[0] < 3.2:
        # print("I executed Here")
        # ZIP Load Step at the individual Buses...
        network.Loads = [
            ExponentialRecoveryLoad(
                (127.6, 75.3),
                [0.3, 1],
                (1.0, 0.5),
                (1.0),
                (2.26, 5.22),
                (0.38, 2.68)
            ),
            ExponentialRecoveryLoad(
                (127.6, 75.3),
                [0.3, 1],
                (1.0, 0.5),
                (1.0),
                (2.26, 5.22),
                (0.38, 2.68)
            ),
            ExponentialRecoveryLoad(
                (127.6, 75.3),
                [0.3, 1],
                (1.0, 0.5),
                (1.0),
                (2.26, 5.22),
                (0.38, 2.68)
            ),
            ExponentialRecoveryLoad(
                (127.6, 75.3),
                [0.3, 1],
                (1.0, 0.5),
                (1.0),
                (2.26, 5.22),
                (0.38, 2.68)
            )
        ]
    # else:
    #     network.Loads = [
    #         FreqDependentLoad(
    #             0.7,
    #             -2.3,
    #             377,
    #             ExponentialLoad(
    #                 P0=0.09,
    #                 Q0=0.0436,
    #                 V0=1.0,
    #                 np=1.2,
    #                 nq=2.7
    #             )
    #         ),
    #         FreqDependentLoad(
    #             0.7,
    #             -2.3,
    #             377,
    #             ExponentialLoad(
    #                 P0=0.135,
    #                 Q0=0.0654,
    #                 V0=1.0,
    #                 np=1.2,
    #                 nq=2.7
    #             )
    #         ),
    #         FreqDependentLoad(
    #             0.7,
    #             -2.3,
    #             377,
    #             ExponentialLoad(
    #                 P0=0.09,
    #                 Q0=0.0436,
    #                 V0=1.0,
    #                 np=1.2,
    #                 nq=2.7
    #             )
    #         ),
    #         FreqDependentLoad(
    #             0.7,
    #             -2.3,
    #             377,
    #             ExponentialLoad(
    #                 P0=0.5,
    #                 Q0=0.0872,
    #                 V0=1.0,
    #                 np=1.2,
    #                 nq=2.7
    #             )
    #         ),
    #     ]
    pass