# Internal Imports
from LoadModels.StaticLoads import ZIPpolynomialLoad, FreqDependentLoad, ExponentialLoad
from GenerationModels.InverterModel import SinglePhaseInverter
from NetworkModel.LowVoltageNetwork import LowVoltageNetwork
from ThesisSimulations.LoadStepCase2.BusSettings import *
from NetworkPlotter.PowerNetworkPlotter import *
# External Imports
import numpy as np


# Define Simulation to be Executed in Main...
def SimulateLVN_Case2(t_sim):
    # Define Time Array for Simulation
    ts = np.linspace(0, t_sim, 5000000)
    # Define Bus Array & Build Bus Objects
    bus = [Bus0(), Bus1(), Bus2(), Bus3()]
    # Define Network Connections & Coupling Between Buses
    connections = NetworkCoupling()
    # Setup Low Voltage Network Simulation Environment
    network = LowVoltageNetwork(
        4,
        50000,
        240,
        [
            bus[0].generation,
            bus[1].generation,
            bus[2].generation,
            bus[3].generation
        ],
        [
            bus[0].initLoad,
            bus[1].initLoad,
            bus[2].initLoad,
            bus[3].initLoad
        ]
    )
    # Establish Connections
    network.Y = connections.Y
    # Get Initial States Based on Defined Network
    initialStates = network.getGenInitStates()
    # Run Simulation...
    results, frequency, loads, simbreakpoint = network.SimulateNetwork(
        ts,
        initialStates[0],
        initialStates[1],
        bus,
        1.8,
        LoadStep,
        returnloads=True
    )
    print("this was the sim breakpoint", simbreakpoint)
    # Display Results...
    PlotResults(ts, t_sim, results, frequency, loads, simbreakpoint)
    return


# Define Network Disturbance Function
def LoadStep(network, t, bus):
    if 2.2 <= t[0] < 2.4:
        network.Loads[0] = bus[0].loadStep2
    elif 2.4 <= t[0] < 2.6:
        network.Loads[1] = bus[1].loadStep2
    elif 2.8 <= t[0] < 3.0:
        network.Loads[2] = bus[2].loadStep2
    elif 3.0 <= t[0] < 3.2:
        network.Loads[3] = bus[3].loadStep
    elif t[0] > 4.0:
        network.Loads = [
            bus[0].initLoad,
            bus[1].initLoad,
            bus[2].initLoad,
            bus[3].initLoad
        ]
    pass
    return


# Define Network Results Plotter
def PlotResults(ts, t_sim, results, frequency, loads, simbreakpoint):
    plotter = Ieee1547Plotter
    # Display Results
    plotter.plotNetworkFrequency(ts[:simbreakpoint], np.array(frequency), showplot=True)
    plotter.plotMultiBusActivePower(ts[:simbreakpoint+1], loads[:, :, 0], showplot=True)
    plotter.plotMultiBusReactivePower(ts[:simbreakpoint+1], loads[:, :, 1], showplot=True)
    plotter.plotMultiBusPhaseError(ts[:simbreakpoint], np.array(results[:, 0:4]), np.array(results[:, 0]), showplot=True)
    plotter.plotNetworkVoltages(ts[:simbreakpoint], np.array(results[:, 4:8]), showplot=True)
    plotter.plotNetworkPhase(ts[:simbreakpoint], np.sin(np.array(results[:, 0:3])), showplot=True)
    plotter.plotNetworkPhase(ts[:simbreakpoint], np.array(results[:, 0:4]), showplot=True)

    # Plot Results Based on IEEE1547 Req's
    plotter.plotCatfreq_ridethrough(ts[:simbreakpoint], (np.array(frequency)/(2*np.pi)), t_sim)
    plotter.plotCatIII_voltage(ts[:simbreakpoint], np.array(results[:, 4:8]), t_sim)

    return
