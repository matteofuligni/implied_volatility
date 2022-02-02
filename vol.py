import configparser
import numpy as np
import func
from time import time

# Loading of settings
config = configparser.ConfigParser()
config.read('configuration.txt')
RiskFreeReturn = float(config.get('settings', 'R'))
Volatility = float(config.get('settings', 'Volatility'))
InitialAssetPrice = 1
MaxTime = 2
MaxStrike = 1.5
TimesArrayIntervals = 10
StrikesArrayIntervals = 10
SimulationNumbers = 10000
IntervalsNumber = 10000
MaxIteration = 10000
Precision = 1.0e-8

# Create the array for strike and time
TimesArray = np.linspace(0.5, MaxTime, TimesArrayIntervals)
StrikeArray = np.linspace(0.5, MaxStrike, StrikesArrayIntervals)

# Create the meshgrid
StrikesMeshgrid, TimesMeshgrid = np.meshgrid(StrikeArray, TimesArray)
VolatilityMatrix = np.empty(shape=(TimesArrayIntervals, StrikesArrayIntervals))

# Set the random seed
np.random.seed(20000)

# Fix the zero time
InitialTime = time()

# Compute the price matrix
PricesMatrix = func.generatePricesMatrix(TimesArray, StrikeArray, IntervalsNumber, SimulationNumbers,
                               InitialAssetPrice, RiskFreeReturn, Volatility)

# Find the implied volatility matrix
for i in range(len(TimesArray)):
    for j in range(len(StrikeArray)):
        VolatilityMatrix[i,j] = func.findImpliedVolatility(PricesMatrix[i,j], InitialAssetPrice, StrikeArray[j],
                                                           TimesArray[i], RiskFreeReturn, MaxIteration, Precision)

# Total time
print('All Done! Time: ', round(time()-InitialTime, 2))

# Price Chart
func.price_chart(StrikesMeshgrid, TimesMeshgrid, PricesMatrix)
# Volatility Chart
func.volatility_chart(StrikesMeshgrid, TimesMeshgrid, VolatilityMatrix)
