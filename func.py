import numpy as np
from scipy import stats
import warnings
from datetime import datetime


def computeSinglePrice(DeltaTime, Strike, IntervalsNumber, SimulationNumbers, InitialAssetPrice,
                       RiskFreeReturn, Volatility, AttualizationFactor, NormalMatrix):
    """ Compute a single Call Price
        This method implement the Monte Carlo and Euler methods to compute
        the expectation value of the price of a call option given the input parameters

        Parameters
            DeltaTime : the amplitude of a each time intervals
            Strike : the value of the strike for the Call
            IntervalsNumber : the number of intervals for the Euler method
            SimulationNumbers : the number of simulation for the Montecarlo method
            InitialAssetPrice : the initial price of the underlying asset
            RiskFreeReturn : the risk-free return refered to the bank account
            Volatility : the volatility of the underlying asset
            AttualizationFactor : the factor that has to applied to the payoff to obtain the price
            NormalMatrix : a matrix of normal obsevation with dimensions IntervalsNumber x SimulationNumbers

        Returns
            The expectation value of the Call price given the parameters
    """
    PriceArray = np.empty((SimulationNumbers)); PriceArray.fill(InitialAssetPrice)
    VolatilityArray = np.empty((SimulationNumbers)); VolatilityArray.fill(Volatility)
    for j in range(IntervalsNumber):
        dw = np.sqrt(DeltaTime)*NormalMatrix[j,:]
        PriceArray = PriceArray*(1+RiskFreeReturn*DeltaTime)+np.multiply(VolatilityArray,dw)
        Payoff = np.maximum(PriceArray-Strike,0).mean()
    return Payoff*AttualizationFactor

def generatePricesMatrix(TimesArray, StrikeArray, IntervalsNumber,
                         SimulationNumbers, InitialAssetPrice, RiskFreeReturn,
                         Volatility):
    """ Call prices matrix
        This method implement the Monte Carlo and Euler methods to compute
        the expectation value of all the prices of a call option by varying
        the expiration time and the strike.

        Parameters
            TimesArray : an array with all the possible expiration times
            StrikeArray : an array with all the possible strike
            IntervalsNumber : the number of interval in which the trajectory
                      of the underlying asset has been divided to
                      implement the Euler scheme
            SimulationNumbers : the number of montecarlo simulations
            InitialAssetPrice : the initial value of the asset
            RiskFreeReturn : the value of the risk-free return
            Volatility : the value of the fixed volatility of the asset

        Returns
            The PricesMatrix matrix with all the computed prices
    """
    InitialTime = datetime.now()
    PricesMatrix = np.zeros(shape=(len(TimesArray),len(StrikeArray)))
    NormalMatrix = stats.norm.rvs(size=(IntervalsNumber,SimulationNumbers))
    print('Normal Generated! Time: ', datetime.now()-InitialTime)
    for i in range(len(TimesArray)):
        T = TimesArray[i]; DeltaTime = T/IntervalsNumber; AttualizationFactor=np.exp(-RiskFreeReturn*T)
        for g in range(len(StrikeArray)):
            PricesMatrix[i,g] = computeSinglePrice(DeltaTime, StrikeArray[g], IntervalsNumber, SimulationNumbers,
                                                   InitialAssetPrice, RiskFreeReturn, Volatility, AttualizationFactor,
                                                   NormalMatrix)
            PassedTime = datetime.now() - InitialTime
            print('Done element in position [', i, ']','[',g,']', 'Time: ', PassedTime)
    return PricesMatrix


def blackScholesCallPrice(InitialAssetPrice, Strike, Time, RiskFreeReturn, Volatility):
    """ Call price Blcak-Scholes
        This method implements the Black-Scholes formula
        to compute the price of a call option given the strike,
        the expiration time, the risk-free return and the volatility

        Parameters
            InitialAssetPrice : the initial value of the assets
            Strike : the strike of the option
            Time : the option expiration time
            RiskFreeReturn : the risk-free return
            Volatility : the volatility of the asset

        Returns
            The price of the call option
    """
    CallPrice = 0
    with np.errstate(divide='ignore', invalid='ignore'):
        d1 = np.nan_to_num(np.divide((np.log(InitialAssetPrice/Strike) +
             (RiskFreeReturn + 0.5*Volatility**2)*Time),(Volatility*np.sqrt(Time))))
        d2 = d1 - Volatility * np.sqrt(Time)
        CallPrice = InitialAssetPrice * stats.norm.cdf(d1) - np.exp(-RiskFreeReturn * Time) * Strike * stats.norm.cdf(d2)
        if np.isnan(CallPrice):
            return 0.0
    return CallPrice


def blackScholesVegaGreek(InitialAssetPrice, Strike, Time, RiskFreeReturn, Volatility):
    """ Compute value Vega greek
        This method implements the formula to compute the greek
        vega, that is the derivative of the Black-Scholes
        formula with respect to the price, utilized in the find_vol
        function.

        Parameters
            InitialAssetPrice : the initial value of the assets
            Strike : the strike of the option
            Time : the option expiration time
            RiskFreeReturn : the risk-free return
            Volatility : the volatility of the asset

        Returns
            The value of the Vega greek derivative
    """
    VegaGreek = 0
    with np.errstate(divide='ignore', invalid='ignore'):
        d1 = np.divide((np.log(InitialAssetPrice / Strike) +
            (RiskFreeReturn + 0.5 * Volatility ** 2) * Time),(Volatility * np.sqrt(Time)))
        VegaGreek = InitialAssetPrice * stats.norm.pdf(d1) * np.sqrt(Time)
    return VegaGreek


def findImpliedVolatility(TargetValue, InitialAssetPrice, Strike, Time, RiskFreeReturn, MaxIteration, Precision):
    """ Implied volatility Newton-Raphson
        This method implements the Newton-Raphson method to
        compute the implied volatility for the input price.

        Parameters
            TargetValue : the price of which we want to compute
                           the Black-Scholes volatility
            InitialAssetPrice : the initial value of the assets
            Strike : the strike of the option
            Time : the option expiration time
            RiskFreeReturn : the risk-free return
            MaxIteration : max number of iterations
            Precision : the precision respect to the target value

        Returns
            The value of the implied volatility for that time and strike
        """
    ImpliedVolatility = 0.3
    for i in range(0, MaxIteration):
        CallPrice = blackScholesCallPrice(InitialAssetPrice, Strike, Time, RiskFreeReturn, ImpliedVolatility)
        VegaGreek = blackScholesVegaGreek(InitialAssetPrice, Strike, Time, RiskFreeReturn, ImpliedVolatility)
        Difference = TargetValue - CallPrice
        if (abs(Difference) < Precision):
            return np.float64(ImpliedVolatility)
        ImpliedVolatility = ImpliedVolatility + np.divide(Difference,VegaGreek)
    warnings.warn("Max Number of Iterations Reached")
    return ImpliedVolatility
