# Internal Imports
from ThesisSimulations.LoadStepCase1.Simulation import SimulateLVN_Case1

# External Imports
import numpy as np

'''Main is used to run the desired test Modules as pleased....'''

if __name__ == '__main__':
    print("Running Main Simulation Script")
    # Run Network Dynamic Simulation Case 1
    SimulateLVN_Case1(5)
    # # Run Network Unit Test
    # simLVN_ThesisCase1(
    #     np.linspace(0.1, T_tot, N)
    # )
    # simLVN_ThesisCase2(
    #     np.linspace(0.1, T_tot, N)
    # )
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
    # simLVN_ERLLoadsCase1(
    #     np.linspace(0.0, T_tot, N),
    #     T_tot
    # )
    print("I am done... Happy Analyzing :)")
    pass
