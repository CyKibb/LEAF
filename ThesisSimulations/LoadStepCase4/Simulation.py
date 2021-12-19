# Internal Imports
from LoadModels.StaticLoads import ZIPpolynomialLoad, FreqDependentLoad, ExponentialLoad
from GenerationModels.InverterModel import SinglePhaseInverter
from NetworkModel.LowVoltageNetwork import LowVoltageNetwork
from ThesisSimulations.LoadStepCase4.BusSettings2 import *
from NetworkPlotter.PowerNetworkPlotter import *
# External Imports
import numpy as np


# Define Simulation to be Executed in Main...
def SimulateLVN_Case4(t_sim):
    # Define Time Array for Simulation
    ts = np.linspace(0, t_sim, 10000)
    # Define Bus Array & Build Bus Objects
    bus = [Bus0(), Bus1(), Bus2(), Bus3()]
    # Define Network Connections & Coupling Between Buses
    connections = Network()
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
        1.45,
        LoadStep,
        returnloads=True
    )
    print("this was the sim breakpoint", simbreakpoint)
    # Display Results...
    PlotResults(ts, t_sim, results, frequency, loads, simbreakpoint)
    PlotBusPowerResponse(
        np.linspace(0, t_sim, np.array(network.GeneratorActivePowerOutput).shape[0] + 1),
        np.squeeze(np.array(network.GeneratorActivePowerOutput), axis=2),
        np.squeeze(np.array(network.GeneratorReactivePowerOutput), axis=2)
    )
    PlotBusPowerResponse(
        np.linspace(0, t_sim, np.array(network.GeneratorActivePowerOutput).shape[0] + 1),
        np.array(network.NetworkActivePower),
        np.array(network.NetworkReactivePower)
    )
    return


# Define Network Disturbance Function
def LoadStep(network, t, bus):
    if 1.5 <= t[0] < 240:
        network.Loads[0] = bus[0].loadStep
    elif 300 <= t[0] < 600:
        network.Loads[1] = bus[1].loadStep
    elif 700 <= t[0] < 1000:
        network.Loads[2] = bus[2].loadStep
    elif 1000 <= t[0] < 1800:
        network.Loads[3] = bus[3].loadStep
    return


def LoadStep2(network, t, bus):
    if 2000 <= t[0] < 2100:
        network.Loads = [
            bus[0].loadStep,
            bus[1].loadStep,
            bus[2].loadStep,
            bus[3].loadStep
        ]
    return


# Define Network Results Plotter
def PlotResults(ts, t_sim, results, frequency, loads, simbreakpoint):
    plotter = Ieee1547Plotter

    # Plot Results Based on IEEE1547 Req's
    plotter.plotCatfreq_ridethrough(ts[:simbreakpoint], (np.array(frequency) / (2 * np.pi)), t_sim)
    plotter.plotCatIII_voltage(ts[:simbreakpoint], np.array(results[:, 4:8]), t_sim)

    # Display Detailed Results
    plotter.plotNetworkFrequency(ts[:simbreakpoint + 1], np.array(frequency), showplot=True)
    plotter.plotActivePowerLoading(ts[:simbreakpoint + 1], loads[:, :, 0], showplot=True)
    plotter.plotReactivePowerLoading(ts[:simbreakpoint + 1], loads[:, :, 1], showplot=True)
    plotter.plotMultiBusPhaseError(ts[:simbreakpoint], np.array(results[:, 0:4]),
                                   np.array(results[:, 0]), showplot=True)
    # plotter.plotNetworkVoltages(ts[:simbreakpoint], np.array(results[:, 4:8]), showplot=True)
    # plotter.plotNetworkPhase(ts[:simbreakpoint], np.sin(np.array(results[:, 0:3])), showplot=True)
    plotter.plotNetworkPhase(ts[:simbreakpoint], np.array(results[:, 0:4]), showplot=True)
    return


def PlotBusPowerResponse(ts, busActivePower, busReactivePower):
    plotter = Ieee1547Plotter

    plotter.plotMultiBusActivePower(ts, busActivePower, showplot=True)
    plotter.plotMultiBusReactivePower(ts, busReactivePower, showplot=True)

    return