import numpy as np
from numpy.core.defchararray import index
from scipy.integrate.odepack import odeint
from GenerationModels.InverterModel import SinglePhaseInverter
from LoadModels.StaticLoads import ZIPpolynomialLoad


class LowVoltageNetwork:
    """ --------------------
    docstring for low-voltage network class
    ""
    Note:
    The dynamics and set points of the inverter should adhere to the
    IEEE 1547-2018 requirements

    TODO:
    Left Off Point: Need to adjust the return value from getNextState
    1. Adjust Dynamic Models so they fit into the simulation properly
    2. Change everything so the user defines Sbase and Vbase and the results
        are given in the p.u.
    3. Adjust getinitstate and wrapper to properties

    -------------------------"""

    def __init__(self, NodeNums, Sbase, Vbase, Generation, Loads):
        # Static Attirubtes of the network (Public)
        self.NodeNums = NodeNums
        self.Sbase = Sbase
        self.Vbase = Vbase
        # Static Attirubtes of the network (Private)
        self.__Nflow = -1 * np.ones(
            (NodeNums, NodeNums))  # Power Flow Matrix to account for how power flows amongst buses
        np.fill_diagonal(self.__Nflow, 1)
        # TODO: ADJUST THE MATRIX MULTIPLICATION TO INCLUDE THIS NUMBER
        # User Defined Generation and Load at Network Buses
        self.Generation = Generation  # Generation Vecotr Containing Generation Objects
        self.Loads = Loads  # Load Vector Containing Load Objects
        # Dynamic Attributes Initialization of the network (Public)
        self.Ebus = np.zeros((NodeNums, 1))  # Network Bus Voltage Vector
        # Dynamic Attributes Initialization of the network (Private)
        self.__Y = np.zeros((NodeNums, NodeNums))  # Network Coupling (Cartesian)
        self.__Ymag = np.zeros((NodeNums, NodeNums))  # Network Coupling (Polar MAGNITUDE)
        self.__Yang = np.zeros((NodeNums, NodeNums))  # Network Coupling (Polar ANGLE)
        self.__Theta = np.zeros((NodeNums, NodeNums))  # Phase Coupling Matrix
        self.__Phi = np.zeros((NodeNums, NodeNums))  # Phase Coupling Matrix
        self.__Kappa = np.zeros((NodeNums, 1))  # Network Bus Coupling Gain (Ebk*Ebj*Ybkj)
        self.__Snwk = np.zeros((NodeNums, 2))  # Snetwork Exported to other nodes vector representation
        self.__Pnwk = np.zeros((NodeNums, 1))  # Qnetwork Exported to other nodes vector representation
        self.__Qnwk = np.zeros((NodeNums, 1))  # Qnetwork Exported to other nodes vector representation
        print("Low Voltage Network Created!")

    """ User Must Pass In the Desired Coupling Impedances Between Busses """

    @property
    def Y(self):
        return self.__Y

    @Y.setter
    def Y(self, Ycoupling):
        self.__Y = Ycoupling
        self.__Ymag = np.absolute(self.__Y)
        self.__Yang = np.angle(self.__Y)
        # np.fill_diagonal(self.__Y, 0)                       # Ensure Diag(Y) is zero for loads

    @property
    def Phi(self):
        return self.__Phi

    @Phi.setter
    def Phi(self, Theta):
        ThetaM = np.tile(Theta, self.NodeNums)
        self.__Phi = ThetaM - ThetaM.T + self.__Yang  # Adjustment was made from - -> + on Yang

    @property
    def Snwk(self):
        return self.__Snwk

    @Snwk.setter
    def Snwk(self, E):
        # This is technically not Kappakj just yet :)...
        self.__Kappa = np.multiply(
            self.__Nflow,
            np.matmul(
                np.diag(E[:, 0]),
                self.__Ymag
            )
        )
        self.__Pnwk = np.matmul(
            np.multiply(
                self.__Kappa,
                np.cos(self.__Phi)
            ),  # The question here is if the transpose is happening first?
            E
        )
        self.__Qnwk = np.matmul(
            np.multiply(
                self.__Kappa,
                np.sin(self.__Phi)
            ),
            E
        )

    @property
    def getNextStateWrapper(self):
        return lambda State, t, f, t_int, busloadpowers: self.getNextState(State, t, f, t_int, busloadpowers)

    # Should be change to a property for future reference :/
    def getGenInitStates(self):
        init_voltage = []
        init_phase = []
        init_frequency = []
        for Index in self.Generation:
            InitialStates = Index.getInitStates()
            init_phase.append(InitialStates[0])
            init_voltage.append(InitialStates[1])
            init_frequency.append(InitialStates[2])
        return init_phase + init_voltage, init_frequency

    """ Note State format of State[:Nodenums/2] = phase & State[Nodenums/2 :] = Voltage """

    def getNextState(self, State, t, f, t_int, busloadpowers):
        # Update Phase Angle and Network Coupling State Matrices (Reshape to Column Vectors)
        self.Phi = np.array(State[0:self.NodeNums]).reshape((self.NodeNums, 1))
        self.Snwk = np.array(State[self.NodeNums:2 * self.NodeNums]).reshape((self.NodeNums, 1))
        # Prepare Next States Row Vectors
        dEdt = []
        dThetadt = []
        # Calculate Next States for Each Node in Network
        for i in range(0, self.NodeNums):
            BusIndex = [i, i + self.NodeNums]
            GenerationNextState = self.Generation[i].getNextState(
                [State[index] for index in BusIndex],
                t,
                self.__Pnwk[i][0] + busloadpowers[i][0],
                self.__Qnwk[i][0] + busloadpowers[i][1]
            )  # GenerationNextState
            dEdt.append(GenerationNextState[0])
            dThetadt.append(GenerationNextState[1])
        return dThetadt + dEdt

    def __NetworkIntegrator(self, t, initialStates, f, t_int, busloads):
        return odeint(self.getNextStateWrapper, initialStates, t, args=(f, t_int, busloads))

    """ NOTE: 
        -   State layout [theta: 0 -> nodes_nums, Voltage: node_nums -> 2*node_nums] 
        -   tload: is the timing for the disturbance function to begin execution
        -   loadfunc: is the disturbance load function to be passed in to be executed at tload.
        -   Looping Optimization on ODEint may need to be addressed?? for faster run time?
        -   To optimize for simulation time we need to switch loops to build in operations or numpy functions
    """
    def SimulateNetwork(self, ts, initialstates, init_frequency, tload=None, loadfunc=None, returnloads=False):
        # Append Initial States to Final System Response
        response = [initialstates]
        frequency = [np.array(init_frequency)]
        nwkloading = []
        # Integrate Network Dynamics Across Each Time Step ts
        for i in range(len(ts) - 1):
            # Time step for integrator
            t = [ts[i], ts[i + 1]]
            # Get load power to run integration over at the timestamp
            busloadpowers = []
            for j in range(0, self.NodeNums):
                busloadpowers.append(
                    self.Loads[j].getLoadPower(
                        response[i][self.NodeNums + j],  # Pass in the voltage to calculate load power
                        frequency[i][j],  # Pass in the bus frequency to calculate load power
                        t  # Pass in the time for dynamic loads in the nwk
                    )
                )
            # Check to see user wants returned bus load powers from sim
            if returnloads is True:
                nwkloading.append(busloadpowers)
            # Check for Load Step function and execute if exists
            if tload is None:
                pass
            elif t[0] >= tload and loadfunc is not None:
                loadfunc(self, t)
            # Integrate Network States
            states = self.__NetworkIntegrator(t, initialstates, frequency[i], t, busloadpowers)
            # Calculate Generator Frequency
            frequency.append(
                ((states[1, 0:self.NodeNums] - states[0, 0:self.NodeNums]) / (ts[i + 1] - ts[i]))
            )
            # Adjust for Phase State 2pi overflow
            states[1, 0:self.NodeNums] = states[1, 0:self.NodeNums] % (2 * np.pi)
            # Update initial states for next iteration
            initialstates = states[1]
            # Append simulation results list
            response.append(states[1].tolist())
        if returnloads is True:
            return np.array(response), np.array(frequency), np.array(nwkloading)
        else:
            return np.array(response), np.array(frequency)


if __name__ == '__main__':
    # Run Unit Test...
    print("Performing Low Voltage Network Unit Test")