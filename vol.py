import configparser
import numpy as np
import sys
import func as f
import graph as g
from datetime import datetime as dt

# Loading of settings
config = configparser.ConfigParser()
try:
    config.read(sys.argv[1])
except IndexError:
    print ("You did not specify a correct file! The default file will be loaded")
    config.read('configuration.txt')
RiskFreeReturn = float(config.get('settings', 'RiskFreeReturn'))
Volatility = float(config.get('settings', 'Volatility'))
SimulationNumbers = int(config.get('settings', 'SimulationNumbers'))
IntervalsNumber = int(config.get('settings', 'IntervalsNumber'))
MaxIteration = int(config.get('settings', 'MaxIteration'))
Precision = float(config.get('settings', 'Precision'))
RandomSeed = int(config.get('settings', 'RandomSeed'))


InitialAssetPrice = 1
MaxTime = 2
MaxStrike = 1.5
TimesArrayIntervals = 10
StrikesArrayIntervals = 10


# Create the array for strike and time
TimesArray = np.linspace(0.5, MaxTime, TimesArrayIntervals)
StrikeArray = np.linspace(0.5, MaxStrike, StrikesArrayIntervals)

# Create the meshgrid
StrikesMeshgrid, TimesMeshgrid = np.meshgrid(StrikeArray, TimesArray)
VolatilityMatrix = np.empty(shape=(TimesArrayIntervals, StrikesArrayIntervals))

# Set the random seed
np.random.seed(RandomSeed)

# Fix the zero time
InitialTime = dt.now()

# Compute the price matrix
PricesMatrix = f.generatePricesMatrix(TimesArray, StrikeArray, IntervalsNumber, SimulationNumbers,
                               InitialAssetPrice, RiskFreeReturn, Volatility)

# Find the implied volatility matrix
for i in range(len(TimesArray)):
    for j in range(len(StrikeArray)):
        VolatilityMatrix[i,j] = f.findImpliedVolatility(PricesMatrix[i,j], InitialAssetPrice, StrikeArray[j],
                                                           TimesArray[i], RiskFreeReturn, MaxIteration, Precision)

# Total time
print('All Done! Time: ', dt.now()-InitialTime)

# Price Chart
g.generatePriceChart(StrikesMeshgrid, TimesMeshgrid, PricesMatrix)
# Volatility Chart
g.generateImpliedVolatilityChart(StrikesMeshgrid, TimesMeshgrid, VolatilityMatrix)
