import matplotlib.pyplot as plt
from matplotlib import cm

def generatePriceChart(StikesMeshgrid, TimeMeshgrid, PricesMatrix, PricesChartPath):
    """ This method plot the price chart.

        Parameters
            StikesMeshgrid : the strike meshgrid
            TimeMeshgrid : the time meshgrid
            PricesMatrix : the price matrix
        """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(StikesMeshgrid, TimeMeshgrid, PricesMatrix, facecolors=cm.jet(PricesMatrix), lw=0)
    plt.locator_params(axis="x", nbins=5)
    plt.locator_params(axis="y", nbins=5)
    plt.locator_params(axis="z", nbins=5)
    ax.set_xlabel('Strike', fontsize='14')
    ax.set_ylabel('Time', fontsize='14')
    ax.set_zlabel('Price', fontsize='14')
    ax.tick_params(axis='both', which='major', labelsize=10)
    plt.title('Price Chart', fontsize='24')
    plt.savefig(PricesChartPath, dpi = 300)
    plt.show()

def generateImpliedVolatilityChart(StikesMeshgrid, TimeMeshgrid, VolatilityMatrix, VolatilityChartPath):
    """ This method plot the implied volatility chart.

        Parameters
            StikesMeshgrid : the strike meshgrid
            TimeMeshgrid : the time meshgrid
            VolatilityMatrix : the implied volatility matrix
        """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(StikesMeshgrid, TimeMeshgrid, VolatilityMatrix, facecolors=cm.jet(VolatilityMatrix), lw=0)
    plt.locator_params(axis="x", nbins=5)
    plt.locator_params(axis="y", nbins=5)
    plt.locator_params(axis="z", nbins=5)
    ax.set_xlabel('Strike', fontsize='14')
    ax.set_ylabel('Time', fontsize='14')
    ax.set_zlabel('Vol', fontsize='14')
    ax.tick_params(axis='both', which='major', labelsize=10)
    plt.title(' Volatility Chart', fontsize='24')
    plt.savefig(VolatilityChartPath, dpi = 300)
    plt.show()
