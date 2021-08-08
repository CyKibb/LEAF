# Internal Imports
from NetworkTestCases.Synchronization.SyncCase1 import *
from NetworkTestCases.StaticLoads.ZIPLoadTests.ZIPLoadCase1 import *
from NetworkTestCases.StaticLoads.ZIPLoadTests.ZIPLoadCase2 import *
from NetworkTestCases.StaticLoads.ExponentialLoadsTests.EXPLoadCase1 import *
from NetworkTestCases.StaticLoads.FreqDependentLoadsTests.FreqLoadCase1 import *
from NetworkTestCases.StaticLoads.EPRILoadsTests.EPRILoadCase1 import *
from NetworkTestCases.DynamicLoads.ERLLoadCase1 import *

# External Imports
import numpy as np


'''Main is used to run the desired test Modules as pleased....'''

if __name__ == '__main__':
    print("Running Main Simulation Script")
    # Define Number of Sample Pointer required
    N = 1000
    # # Simulation Total Time (s)
    T_tot = 5
    # Run Network Unit Test
    # simLVN_Synchronization(
    #     np.linspace(0.0, T_tot, N)
    # )
    # simLVN_ZIPLoadsCase1(
    #     np.linspace(0.0, T_tot, N)
    # )
    # simLVN_ZIPLoadsCase2(
    #     np.linspace(0.0, T_tot, N)
    # )
    # simLVN_EXPLoadsCase1(
    #     np.linspace(0.0, T_tot, N)
    # )
    # simLVN_FreqLoadsCase1(
    #     np.linspace(0.0, T_tot, N)
    # )
    # simLVN_EPRILoadsCase1(
    #     np.linspace(0.0, T_tot, N)
    # )
    simLVN_ERLLoadsCase1(
        np.linspace(0.0, T_tot, N),
        T_tot
    )
    print("I am done... Happy Analyzing :)")
    pass
