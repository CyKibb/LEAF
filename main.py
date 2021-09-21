# Internal Imports
from ThesisSimulations.LoadStepCase1.Simulation import SimulateLVN_Case1

# External Imports
import numpy as np

from ThesisSimulations.LoadStepCase2.Simulation import SimulateLVN_Case2

'''Main is used to run the desired test Modules as pleased....'''

if __name__ == '__main__':
    print("Running Main Simulation Script")
    # Run Network Dynamic Simulation Case 1
    # SimulateLVN_Case1(5)
    # states = [1,-1,1,1]
    #
    # print((True for state in states if state == 0))
    # print(any(True for state in states if state < 0))
    SimulateLVN_Case2(5)

    print("I am done... Happy Analyzing :)")
    pass
