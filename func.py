import numpy as np
from scipy import stats
from datetime import datetime

def sigma(AssetPrice, Volatility):
    """ This method compute the value of the volatility in the case
        it depends on the price.

        Parameters
            S : the assets price

        Returns
            The value of the volatility """
    volatility = Volatility # A possible alternative could be: np.multiply(.2*np.maximum(1,2-S),S)
    return volatility


def computeSinglePrice(DeltaTime, Strike, IntervalsNumber, SimulationNumbers, InitialAssetPrice,
                RiskFreeReturn, Volatility, AttualizationFactor, NormalMatrix):
    """
    """


    S0 = InitialAssetPrice; R = RiskFreeReturn; VOL = Volatility
    S = np.empty((SimulationNumbers)); S.fill(S0)
    V = V = np.empty((SimulationNumbers)); V.fill(sigma(S0, VOL))
    for j in range(IntervalsNumber):
        dw = np.sqrt(DeltaTime)*NormalMatrix[j,:]
        V = sigma(S, VOL)
        S = S*(1+R*DeltaTime)+np.multiply(V,dw)
        Payoff = np.maximum(S-Strike,0).mean()
    return Payoff*AttualizationFactor

def generatePricesMatrix(TimesArray, StrikeArray, IntervalsNumber,
          SimulationNumbers, InitialAssetPrice, RiskFreeReturn, Volatility):
    """ This method implement the Monte Carlo and Euler methods to compute
        the expectation value of all the prices of a call option by varying
        the expiration time and the strike.

        Parameters
            T_array : an array with all the possible expiration times
            K_array : an array with all the possible strike
            N_INTER : the number of interval in which the trajectory
                      of the underlying asset has been divided to
                      implement the Euler scheme
            S0 : the initial value of the asset
            R : the value of the risk-free return
            VOL : the value of the fixed volatility of the asset

        Returns
            The CC matrix with all the computed prices
    """

    S0 = InitialAssetPrice; R = RiskFreeReturn; Vol = Volatility;
    InitialTime = datetime.now()
    CC = np.zeros(shape=(len(TimesArray),len(StrikeArray)))
    NormalMatrix = stats.norm.rvs(size=(IntervalsNumber,SimulationNumbers))
    print('Normal Generated! Time: ', datetime.now()-InitialTime)
    for i in range(len(TimesArray)):
        T = TimesArray[i]; DeltaTime = T/IntervalsNumber; AttualizationFactor=np.exp(-R*T)
        for g in range(len(StrikeArray)):
            CC[i,g] = computeSinglePrice(DeltaTime, StrikeArray[g], IntervalsNumber, SimulationNumbers,
                                         S0, R, Vol, AttualizationFactor, NormalMatrix)
            PassedTime = datetime.now() - InitialTime
            print('Done : C[', i, ']','[',g,']', 'Time: ', PassedTime)
    return CC


def blackScholesCallPrice(InitialAssetPrice, Strike, Time, RiskFreeReturn, Volatility):
    """ This method implements the Black-Scholes formula
        to compute the price of a call option given the strike,
        the expiration time, the risk-free return and the volatility

        Parameters
            S : the initial value of the assets
            K : the strike of the option
            T : the option expiration time
            r : the risk-free return
            vol : the volatility of the asset

        Returns
            The price of the call option
    """
    S0 = InitialAssetPrice; R = RiskFreeReturn; V = Volatility
    CallPrice = 0
    with np.errstate(divide='ignore', invalid='ignore'):
        d1 = np.nan_to_num(np.divide((np.log(S0/Strike) + (R + 0.5*V**2)*Time),(V*np.sqrt(Time))))
        d2 = d1 - V * np.sqrt(Time)
        CallPrice = S0 * stats.norm.cdf(d1) - np.exp(-R * Time) * Strike * stats.norm.cdf(d2)
        if CallPrice == np.nan:
            return 0.0
    return CallPrice


def blackScholesVegaGreek(InitialAssetPrice, Strike, Time, RiskFreeReturn, Volatility):
    """ This method implements the formula to compute the greek
        vega, that is the derivative of the Black-Scholes
        formula with respect to the price, utilized in the find_vol
        function.

        Parameters
            S : the initial value of the assets
            K : the strike of the option
            T : the option expiration time
            r : the risk-free return
            sigma : the volatility of the asset

        Returns
            The value of the derivative
    """
    S0 = InitialAssetPrice; R = RiskFreeReturn; V = Volatility
    VegaGreek = 0
    with np.errstate(divide='ignore', invalid='ignore'):
        d1 = np.divide((np.log(S0 / Strike) + (R + 0.5 * V ** 2) * Time),(V * np.sqrt(Time)))
        VegaGreek = S0 * stats.norm.pdf(d1) * np.sqrt(Time)
    return VegaGreek


def findImpliedVolatility(TargetValue, InitialAssetPrice, Strike, Time, RiskFreeReturn, MaxIteration, Precision):
    """ This method implements the Newton-Raphson method to
        compute the implied volatility for the input price.

        Parameters
            target_value : the price of which we want to compute
                           the Black-Scholes volatility
            S : the initial value of the assets
            K : the strike of the option
            T : the option expiration time
            r : the risk-free return

        Returns
            The value of the implied volatility for that time and strike
        """
    S0 = InitialAssetPrice; R = RiskFreeReturn
    ImpliedVolatility = 0.3
    for i in range(0, MaxIteration):
        CallPrice = blackScholesCallPrice(S0, Strike, Time, R, ImpliedVolatility)
        VegaGreek = blackScholesVegaGreek(S0, Strike, Time, R, ImpliedVolatility)
        Difference = TargetValue - CallPrice
        if (abs(Difference) < Precision):
            return np.float64(ImpliedVolatility)
        ImpliedVolatility = ImpliedVolatility + np.divide(Difference,VegaGreek)

    ##### Add Warning ####
    print('Sigma not found')

    return ImpliedVolatility
