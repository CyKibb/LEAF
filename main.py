# External Imports
import numpy as np

# Internal Imports
from ThesisSimulations.LoadStepCase1.Simulation import SimulateLVN_Case1
from ThesisSimulations.LoadStepCase1_2.Simulation import SimulateLVN_Case1_2
from ThesisSimulations.LoadStepCase2.Simulation import SimulateLVN_Case2
from ThesisSimulations.LoadStepCase3.Simulation import SimulateLVN_Case3
from ThesisSimulations.LoadStepCase4.Simulation import SimulateLVN_Case4

'''Main is used to run the desired test Modules as pleased....'''

if __name__ == '__main__':
    print("Running Main Simulation Script")

    # Run Network Dynamic Simulation Case 1
    # SimulateLVN_Case1(5)

    # Run Network Dynamic Simulation Case 1
    SimulateLVN_Case1_2(5)

    # Run Network Dynamic Simulation Case 2
    # SimulateLVN_Case2(5)

    # Run Network Dynamic Simulation Case 3
    # SimulateLVN_Case3(6)

    # Run Network Dynamic Simulation Case 4
    # SimulateLVN_Case4(5000)

    print("I am done... Happy Analyzing :)")
    pass
