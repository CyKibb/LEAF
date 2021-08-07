import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


class LVNetworkPlotter(object):
    """
    docstring for LV Network Plotter

    *This class provides all plot methods needed to display required network
    bus information that regards stability analysis.

    Note: I may be missing some items (work in progress :))

    """
    @staticmethod
    def plotSingleBus(x, y):
        plt.plot(x, y, color='dodgerblue')
        return plt.show()

    @staticmethod
    def plotMultiBus(x, y):
        for i in range(0, y.shape[1]):
            plt.plot(
                x[0:],  # The [1] needs to be adjusted (this is because initial state)
                y[:, i],
                label=r'$Bus_%i$' % (i)
            )
        plt.legend()
        return plt.show()

    @staticmethod
    def plotNetworkVoltages(x, y):
        for i in range(0, y.shape[1]):
            plt.plot(
                x[0:],  # The [1] needs to be adjusted (this is because initial state)
                y[:, i],
                label=r'$V_{bus_%i}$' % (i)
            )
        plt.xlabel("Time (s)", fontsize=22, style='italic')
        plt.ylabel('Voltage (p.u.)', fontsize=22, style='italic')
        plt.legend()
        return plt.show()

    @staticmethod
    def plotMultiBusPhaseError(x, y, refbus):
        for i in range(0, y.shape[1]):
            plt.plot(
                x[0:],  # The [1] needs to be adjusted (this is because initial state)
                y[:, i] - refbus[:],
                label=r'$\theta_{ref} - \theta_%i$' % (i)
            )
        plt.xlabel("Time(s)", fontsize=22, style='italic')
        plt.ylabel('Phase Error(radians)', fontsize=22, style='italic')
        plt.legend()
        return plt.show()

    @staticmethod
    def plotNetworkFrequency(x, y):
        for i in range(0, y.shape[1]):
            plt.plot(
                x[0:],  # The [1] needs to be adjusted (this is because initial state)
                y[:, i],
                label=r'$f_%i$' % (i)
            )
        plt.xlabel("Time(s)", fontsize=22, style='italic')
        plt.ylabel('Frequency(radians/s)', fontsize=22, style='italic')
        plt.legend()
        return plt.show()

    @staticmethod
    def plotNetworkPhase(x, y):
        for i in range(0, y.shape[1]):
            plt.plot(
                x[0:],  # The [1] needs to be adjusted (this is because initial state)
                y[:, i],
                label=r'$\theta_%i$' % (i)
            )
        plt.xlabel("Time(s)", fontsize=22, style='italic')
        plt.ylabel('Phase(radians)', fontsize=22, style='italic')
        plt.legend()
        return plt.show()