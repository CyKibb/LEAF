import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class LVNetworkPlotter(object):
    """
    docstring for LV Network Plotter

    *This class provides all plot methods needed to display required network
    bus information that regards stability analysis.

    Note: I may be missing some items (work in progress :))

    """
    gridlinewidth = 0.1
    plotlinewidth = 1
    ticksfontsize = 20
    axesfontsize = 22

    @staticmethod
    def plotSingleBus(x, y, showplot=False, *args):
        plt.plot(x, y)
        plt.grid(color='black', linestyle='-', linewidth=LVNetworkPlotter.gridlinewidth)
        if showplot is False:
            return
        else:
            return plt.show()

    @staticmethod
    def plotMultiBus(x, y, showplot=False, *args):
        for i in range(0, y.shape[1]):
            plt.plot(
                x[0:],  # The [1] needs to be adjusted (this is because initial state)
                y[:, i],
                label=r'$Bus_%i$' % (i)
            )
        plt.grid(color='black', linestyle='-', linewidth=LVNetworkPlotter.gridlinewidth)
        plt.legend()
        if showplot is False:
            return
        else:
            return plt.show()

    @staticmethod
    def plotNetworkVoltages(x, y, showplot=False, *args):
        for i in range(0, y.shape[1]):
            plt.plot(
                x[0:],  # The [1] needs to be adjusted (this is because initial state)
                y[:, i],
                label=r'$V_{bus_%i}$' % (i)
            )
        plt.title("Network Bus Voltages Vs. Time", fontsize=LVNetworkPlotter.axesfontsize, style='italic')
        plt.xlabel("Time (s)", fontsize=LVNetworkPlotter.axesfontsize, style='italic')
        plt.ylabel('Voltage (p.u.)', fontsize=LVNetworkPlotter.axesfontsize, style='italic')
        for arg in args:
            plt.gca().add_patch(arg)
        plt.grid(color='black', linestyle='-', linewidth=LVNetworkPlotter.gridlinewidth)
        # plt.xticks(np.arange(0, 5, step=0.05), fontsize=22)
        # plt.yticks(np.arange(0.9, 1.1, step=0.005), fontsize=22)
        plt.legend()
        if showplot is False:
            return
        else:
            return plt.show()

    @staticmethod
    def plotMultiBusPhaseError(x, y, refbus, showplot=False, *args):
        for i in range(0, y.shape[1]):
            plt.plot(
                x[0:],  # The [1] needs to be adjusted (this is because initial state)
                np.sin(y[:, i] - refbus[:]),
                label=r'$\theta_{ref} - \theta_%i$' % (i)
            )
        plt.title("Network Bus Phases (w.r.t Bus 0) Vs. Time", fontsize=LVNetworkPlotter.axesfontsize, style='italic')
        plt.xlabel("Time(s)", fontsize=LVNetworkPlotter.axesfontsize, style='italic')
        plt.ylabel('Phase Error(radians)', fontsize=LVNetworkPlotter.axesfontsize, style='italic')
        plt.grid(color='black', linestyle='-', linewidth=LVNetworkPlotter.gridlinewidth)
        plt.legend()
        if showplot is False:
            return
        else:
            return plt.show()

    @staticmethod
    def plotNetworkFrequency(x, y, showplot=False, *args):
        for i in range(0, y.shape[1]):
            plt.plot(
                x[0:],  # The [1] needs to be adjusted (this is because initial state)
                y[:, i],
                label=r'$f_%i$' % (i)
            )
        plt.title("Network Bus Frequency Vs. Time", fontsize=LVNetworkPlotter.axesfontsize, style='italic')
        plt.xlabel("Time(s)", fontsize=LVNetworkPlotter.axesfontsize, style='italic')
        plt.ylabel('Frequency(Hz)', fontsize=LVNetworkPlotter.axesfontsize, style='italic')
        for arg in args:
            plt.gca().add_patch(arg)
        plt.grid(color='black', linestyle='-', linewidth=LVNetworkPlotter.gridlinewidth)
        plt.legend()
        if showplot is False:
            return
        else:
            return plt.show()
    @staticmethod
    def plotNetworkPhase(x, y, showplot=False, *args):
        for i in range(0, y.shape[1]):
            plt.plot(
                x[0:],  # The [1] needs to be adjusted (this is because initial state)
                y[:, i],
                label=r'$\theta_%i$' % (i)
            )
        plt.title("Network Bus Phase", fontsize=LVNetworkPlotter.axesfontsize, style='italic')
        plt.xlabel("Time(s)", fontsize=LVNetworkPlotter.axesfontsize, style='italic')
        plt.ylabel('Phase(radians)', fontsize=LVNetworkPlotter.axesfontsize, style='italic')
        plt.grid(color='black', linestyle='-', linewidth=LVNetworkPlotter.gridlinewidth)
        plt.legend()
        if showplot is False:
            return
        else:
            return plt.show()
    @staticmethod
    def plotMultiBusActivePower(x, y, showplot=False, *args):
        for i in range(0, y.shape[1]):
            plt.plot(
                x[1:],
                y[:, i],
                label=r'$P_%i$' % (i)
            )
        plt.title("Network Bus Active Power Vs. Time", fontsize=LVNetworkPlotter.axesfontsize, style='italic')
        plt.xlabel("Time(s)", fontsize=LVNetworkPlotter.axesfontsize, style='italic')
        plt.ylabel('Active Power (p.u.)', fontsize=LVNetworkPlotter.axesfontsize, style='italic')
        plt.grid(color='black', linestyle='-', linewidth=LVNetworkPlotter.gridlinewidth)
        plt.legend()
        if showplot is False:
            return
        else:
            return plt.show()

    @staticmethod
    def plotActivePowerLoading(x, y, showplot=False, *args):
        for i in range(0, y.shape[1]):
            plt.plot(
                x[1:],
                y[:, i],
                label=r'$P_%i$' % (i)
            )
        plt.title("Network Bus Active Power Loading Vs. Time", fontsize=LVNetworkPlotter.axesfontsize, style='italic')
        plt.xlabel("Time(s)", fontsize=LVNetworkPlotter.axesfontsize, style='italic')
        plt.ylabel('Active Power (p.u.)', fontsize=LVNetworkPlotter.axesfontsize, style='italic')
        plt.grid(color='black', linestyle='-', linewidth=LVNetworkPlotter.gridlinewidth)
        plt.legend()
        if showplot is False:
            return
        else:
            return plt.show()

    @staticmethod
    def plotMultiBusReactivePower(x, y, showplot=False, *args):
        for i in range(0, y.shape[1]):
            plt.plot(
                x[1:],
                y[:, i],
                label=r'$Q_%i$' % (i)
            )
        plt.title("Network Bus Reactive Power Vs. Time", fontsize=LVNetworkPlotter.axesfontsize, style='italic')
        plt.xlabel("Time(s)", fontsize=LVNetworkPlotter.axesfontsize, style='italic')
        plt.ylabel('Reactive Power (p.u.)', fontsize=LVNetworkPlotter.axesfontsize, style='italic')
        plt.grid(color='black', linestyle='-', linewidth=LVNetworkPlotter.gridlinewidth)
        plt.legend()
        if showplot is False:
            return
        else:
            return plt.show()

    @staticmethod
    def plotReactivePowerLoading(x, y, showplot=False, *args):
        for i in range(0, y.shape[1]):
            plt.plot(
                x[1:],
                y[:, i],
                label=r'$Q_%i$' % (i)
            )
        plt.title("Network Bus Reactive Power Loading Vs. Time", fontsize=LVNetworkPlotter.axesfontsize, style='italic')
        plt.xlabel("Time(s)", fontsize=LVNetworkPlotter.axesfontsize, style='italic')
        plt.ylabel('Reactive Power (p.u.)', fontsize=LVNetworkPlotter.axesfontsize, style='italic')
        plt.grid(color='black', linestyle='-', linewidth=LVNetworkPlotter.gridlinewidth)
        plt.legend()
        if showplot is False:
            return
        else:
            return plt.show()


class Ieee1547Plotter(LVNetworkPlotter):

    @staticmethod
    def plotCatI_voltage(x, y, simtime):
        continuousrect = patches.Rectangle(
            (0, 0.88),
            simtime,
            0.22,
            alpha = 0.1,
            facecolor= "green"
        )
        mandatoryrect = patches.Rectangle(
            (0, 0.65),
            1,
            0.23,
            alpha = 0.1,
            facecolor= "blue",
        )
        permissiverect1 = patches.Rectangle(
            (0, 1.1),
            1,
            0.1,
            alpha = 0.1,
            facecolor= "orange"
        )
        LVNetworkPlotter.plotNetworkVoltages(x, y, True, continuousrect, mandatoryrect, permissiverect1)
        return

    @staticmethod
    def plotCatII_voltage(x, y, simtime):
        continuousrect = patches.Rectangle(
            (0, 0.88),
            simtime,
            0.22,
            alpha=0.1,
            facecolor="green"
        )
        mandatoryrect = patches.Rectangle(
            (0, 0.65),
            5,
            0.23,
            alpha=0.1,
            facecolor="blue"
        )
        permissiverect1 = patches.Rectangle(
            (0, 1.1),
            1,
            0.1,
            alpha=0.1,
            facecolor="orange"
        )
        LVNetworkPlotter.plotNetworkVoltages(x, y, True, continuousrect, mandatoryrect, permissiverect1)
        return

    @staticmethod
    def plotCatIII_voltage(x, y, simtime):
        continuousrect = patches.Rectangle(
            (0, 0.88),
            simtime,
            0.22,
            alpha=0.1,
            facecolor="green"
        )
        mandatoryrect = patches.Rectangle(
            (0, 0.5),
            simtime if simtime < 20 else 20,
            0.38,
            alpha=0.1,
            facecolor="blue"
        )
        permissiverect1 = patches.Rectangle(
            (0, 1.1),
            1,
            0.1,
            alpha=0.1,
            facecolor="orange"
        )
        LVNetworkPlotter.plotNetworkVoltages(x, y, True, continuousrect, mandatoryrect, permissiverect1)
        return

    @staticmethod
    def plotCatfreq_ridethrough(x, y, simtime):
        continuousrect = patches.Rectangle(
            (0, 58.8),
            simtime,
            2.4,
            alpha=0.1,
            facecolor="green"
        )
        mandatoryrect1 = patches.Rectangle(
            (0, 61.2),
            simtime if simtime < 180 else 180,
            0.6,
            alpha=0.1,
            facecolor="blue"
        )
        mandatoryrect2 = patches.Rectangle(
            (0, 57.0),
            simtime if simtime < 180 else 180,
            1.8,
            alpha=0.1,
            facecolor="blue"
        )
        LVNetworkPlotter.plotNetworkFrequency(x, y, True, continuousrect, mandatoryrect1, mandatoryrect2)
        return
