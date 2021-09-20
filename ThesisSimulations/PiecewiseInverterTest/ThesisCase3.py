# Internal Imports
from LoadModels.StaticLoads import FreqDependentLoad, ExponentialLoad
from NetworkPlotter.PowerNetworkPlotter import *
from ThesisSimulations.PiecewiseInverterTest.LVNetwork3 import LVNetwork3Case3Define
from ThesisSimulations.LoadStepCase1.LVNetwork1 import LVNetwork1Case1Define
# External Imports
import numpy as np


def simLVN_ThesisCase3(ts, simtime):
    # Setup Low Voltage Network Simulation Env
    network = LVNetwork3Case3Define()
    # Setup Plotter to Display Results
    initialStates = network.getGenInitStates()
    plotter = LVNetworkPlotter
    results, frequency, Loads = network.SimulateNetwork(
        ts,
        initialStates[0],
        initialStates[1],
        2.8,
        LoadStep,
        returnloads=True
    )

    Ieee1547Plotter.plotCatIII_voltage(ts, np.array(results[:, 4:8]), simtime)
    Ieee1547Plotter.plotCatfreq_ridethrough(ts, (np.array(frequency) / (2 * np.pi)), simtime)
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
        # ZIP Load Step at the individual Buses...
        network.Loads = [
            FreqDependentLoad(
                0.7,
                -2.3,
                377,
                ExponentialLoad(
                    P0=0.1,
                    Q0=0.0736,
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
                    P0=0.035,
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
                    P0=0.1,
                    Q0=0.136,
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
                    P0=0.1,
                    Q0=0.1072,
                    V0=1.0,
                    np=1.2,
                    nq=2.7
                )
            ),
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