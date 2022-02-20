import func as f
import pytest
import numpy as np
import unittest
from hypothesis import given, settings
import hypothesis.strategies as st
from scipy import stats
import random

RandomSeed = 1
IntervalsNumber = 10000
Time = 1
DeltaTime = Time/IntervalsNumber
Strike = 1.5
SimulationNumbers = 10000
InitialAssetPrice = 1
RiskFreeReturn = .05
Volatility = .2
TargetValue = .3
MaxIteration = 10000
Precision = 1.0e-8

np.random.seed(RandomSeed)
AttualizationFactor = np.exp(-RiskFreeReturn*Time)
NormalMatrix = stats.norm.rvs(size=(IntervalsNumber,SimulationNumbers))
OnesMatrix = np.ones(shape=(IntervalsNumber,SimulationNumbers))
ZerosMatrix = np.zeros(shape=(IntervalsNumber,SimulationNumbers))

class Test(unittest.TestCase):

    def test_computeSinglePrice(self):
        """ Test function single price
            Once the normal matrix has been fixed the evolution of price
            is determinits. Here will be tested that the behavior of the function
            is predictable.

            Tests:
            if the result is equal to the expected value
            if doubling the time, the call price increase a bit
            if doubling the initial asset price, the call price increase a lot
            if doubling the Risk-free returns, the call price increase a bit
            if is used an identity matrix to generate the movements of the asset
                that represent an always increasing trajectory with a 20% in volatility
                that could be computed with a deterministic formula
            if is used a zeros matrix to generate the asset movements that represent a
                stationary trajectory with final price 1 and strike 1.5 that should
                generate a price equal to 0
            if the Strike is set equal to 0 then the Call price should be equal to
                the initial asset price
            if the initial asset price is equal to zero then also the call price
                should be equal to zero because the trajectory is identically equal
                to the initial value
            if both the Risk-free return and the volatility are equal to zero, also the
                Call Price should be equal to zero with an initial asset price equal to 1
                and a strike equal to 1.5 beacuase none of the trajectories will pass the
                strike value
        """

        self.assertEqual(f.computeSinglePrice(DeltaTime, Strike, IntervalsNumber,
            SimulationNumbers, InitialAssetPrice, RiskFreeReturn, Volatility,
            AttualizationFactor, NormalMatrix), .0007776785803880014)
        self.assertEqual(f.computeSinglePrice(2*DeltaTime, Strike, IntervalsNumber,
            SimulationNumbers, InitialAssetPrice, RiskFreeReturn, Volatility,
            AttualizationFactor, NormalMatrix), .011535730379362686)
        self.assertEqual(f.computeSinglePrice(DeltaTime, Strike, IntervalsNumber,
            SimulationNumbers, 2*InitialAssetPrice, RiskFreeReturn, Volatility,
            AttualizationFactor, NormalMatrix), .5716803592907251)
        self.assertEqual(f.computeSinglePrice(DeltaTime, Strike, IntervalsNumber,
            SimulationNumbers, InitialAssetPrice, 2*RiskFreeReturn, Volatility,
            AttualizationFactor, NormalMatrix), .0020337465954131818)

        Price = InitialAssetPrice
        for j in range(IntervalsNumber):
            Price = Price*1.000005+0.002
        Payoff = np.maximum(Price-Strike,0).mean()
        Price = Payoff*AttualizationFactor

        self.assertAlmostEqual(f.computeSinglePrice(DeltaTime, Strike, IntervalsNumber,
            SimulationNumbers, InitialAssetPrice, RiskFreeReturn, Volatility,
            AttualizationFactor, OnesMatrix), Price)
        self.assertEqual(f.computeSinglePrice(DeltaTime, Strike, IntervalsNumber,
            SimulationNumbers, InitialAssetPrice, RiskFreeReturn, Volatility,
            AttualizationFactor, ZerosMatrix), 0.0)
        self.assertAlmostEqual(f.computeSinglePrice(DeltaTime, 0, IntervalsNumber,
            SimulationNumbers, InitialAssetPrice, RiskFreeReturn, Volatility,
            AttualizationFactor, NormalMatrix), 1, 2)
        self.assertEqual(f.computeSinglePrice(DeltaTime, Strike, IntervalsNumber,
            SimulationNumbers, 0, RiskFreeReturn, Volatility,
            AttualizationFactor, NormalMatrix), 0)
        self.assertAlmostEqual(f.computeSinglePrice(DeltaTime, Strike, IntervalsNumber,
            SimulationNumbers, InitialAssetPrice, 0, 0,
            AttualizationFactor, NormalMatrix), 0)


    @settings(deadline=None, max_examples=25)
    @given(TimesArray=st.just(np.linspace(0.5, 2, 10)),
           StrikeArray=st.just(np.linspace(0.5, 1.5, 10)),
           IntervalsNumber=st.integers(100,1000),
           SimulationNumbers=st.integers(100,1000))
    def test_generatePricesMatrix(self, TimesArray, StrikeArray, IntervalsNumber, SimulationNumbers):
        """ Test the output type
            This test verify that the output type is a ndarray
            with the right dimensions

            Tests:
            if the return is a multi dimensions array
            if the return array have the right dimensions
        """

        Matrix = f.generatePricesMatrix(TimesArray, StrikeArray, IntervalsNumber,
                                 SimulationNumbers, InitialAssetPrice, RiskFreeReturn,
                                 Volatility)
        assert isinstance(Matrix, np.ndarray) == True
        assert Matrix.shape == (10,10)


    def test_blackScholesCallPrice(self):
        """ Test Black-Scholes formula
            This is the test of the implementation of a deterministic formula,
            so every results have been calculated analytically

            Tests:
            if price is equal to the value computed analytically
            if doubling the initial asset price, the call price should increase a lot
            if doubling the strike, the call price should decrese a lot
            if doubling the time, the call price should increase
            if doubling the volatility, the call price should increase
            if the time is set equal to zero, the call price should be equal to zero
            if the initial asset price is equal to zero, the call price should
                be equal to zero
            if the strike is equal to zero, the call price should be equal
                to the initial asset price
            if the volatility is equal to zero, the call price should be equal to zero
        """
        InitialAssetPrice, Strike = 100, 150
        self.assertAlmostEqual(f.blackScholesCallPrice(InitialAssetPrice, Strike,
            Time, RiskFreeReturn, Volatility), .36, 2)
        self.assertAlmostEqual(f.blackScholesCallPrice(2*InitialAssetPrice, Strike,
            Time, RiskFreeReturn, Volatility), 57.95, 2)
        self.assertAlmostEqual(f.blackScholesCallPrice(InitialAssetPrice, 2*Strike,
            Time, RiskFreeReturn, Volatility), 4.75e-07, 2)
        self.assertAlmostEqual(f.blackScholesCallPrice(InitialAssetPrice, Strike,
            2*Time, RiskFreeReturn, Volatility), 2.34, 2)
        self.assertAlmostEqual(f.blackScholesCallPrice(InitialAssetPrice, Strike,
            Time, 2*RiskFreeReturn, Volatility), 0.64, 2)
        self.assertAlmostEqual(f.blackScholesCallPrice(InitialAssetPrice, Strike,
            Time, RiskFreeReturn, 2*Volatility), 4.84, 2)
        self.assertEqual(f.blackScholesCallPrice(InitialAssetPrice, Strike,
            0, RiskFreeReturn, Volatility), 0.0)
        self.assertEqual(f.blackScholesCallPrice(0, Strike,
            Time, RiskFreeReturn, Volatility), 0.0)
        self.assertEqual(f.blackScholesCallPrice(InitialAssetPrice, 0,
            Time, RiskFreeReturn, Volatility), InitialAssetPrice)
        self.assertEqual(f.blackScholesCallPrice(InitialAssetPrice, Strike,
            Time, RiskFreeReturn, 0), 0.0)

    def test_blackScholesVegaGreek(self):
        """ Test Vega-Greek fromula
            This is a test of the implementation of a deterministic formula,
            all the results have been calculated analytically
        """
        InitialAssetPrice, Strike = 100, 150
        self.assertAlmostEqual(f.blackScholesVegaGreek(InitialAssetPrice, Strike,
            Time, RiskFreeReturn, Volatility), 9.77, 2)
        self.assertAlmostEqual(f.blackScholesVegaGreek(2*InitialAssetPrice, Strike,
            Time, RiskFreeReturn, Volatility), 16.12, 2)
        self.assertAlmostEqual(f.blackScholesVegaGreek(InitialAssetPrice, 2*Strike,
            Time, RiskFreeReturn, Volatility), 7e-05, 2)
        self.assertAlmostEqual(f.blackScholesVegaGreek(InitialAssetPrice, Strike,
            2*Time, RiskFreeReturn, Volatility), 36.32, 2)
        self.assertAlmostEqual(f.blackScholesVegaGreek(InitialAssetPrice, Strike,
            Time, 2*RiskFreeReturn, Volatility), 14.41, 2)
        self.assertAlmostEqual(f.blackScholesVegaGreek(InitialAssetPrice, Strike,
            Time, RiskFreeReturn, 2*Volatility), 31.47, 2)

    @given(Volatility = st.floats(min_value=0.1, max_value=0.9,
                                  allow_nan=False, allow_infinity=False))
    def test_findImpliedVolatility(self, Volatility):
        """ Test implied volatility function
            This is a test that verify that the function can find the right value
            of the implied volatility

            Tests:
            if given any value for the Volatility to compute the Black-Scholes
                Call price, the implied volatility is equal to that volatility
            if increasing the precision and the max number of iterations the
                implied volatility value is almost equal with the passed Volatility
                with increasing precision
        """
        TargetValue = f.blackScholesCallPrice(InitialAssetPrice, Strike,
            Time, RiskFreeReturn, Volatility)
        self.assertAlmostEqual(f.findImpliedVolatility(TargetValue, InitialAssetPrice,
            Strike, Time, RiskFreeReturn, MaxIteration, Precision), Volatility, 3)
        self.assertAlmostEqual(f.findImpliedVolatility(TargetValue, InitialAssetPrice,
            Strike, Time, RiskFreeReturn, 1000000, 1.0e-11), Volatility)


if __name__ == '__main__':
    unittest.main()
