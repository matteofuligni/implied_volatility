# Implied Volatility Surface

## Summary
With this script its possible to generate the implied volatility surface for a defined option with the Euler and Monte Carlo methods.

The implied volatility is the volatility as if that price obtained of an option was calculated with the Black-Scholes model.
The implied volatility surface represent one of the best way to evaluate an option in finance.

## Monte Carlo Method
Monte Carlo Method is a simple technique of numerical approximation of the mean of a random variable X. It is used in many circumstances in mathematica finance and in particular in the pricing problem.

Generally speaking Monte Carlo Method allows approximating the value of an integral numerically. If Y is uniformly distributed on [0,1] and X = f(Y), then the expectation value of X is

E[X] = integral{f(x) dx}

The expectation value of X is the best estimation of the X mean.

This method is used in this project to estimate the prices of an option.

## Euler Method
This method is used here to numerically approximate a stochastic differential equation that regulate the being of an underlying asset.

The Euler scheme implemented in the script are represented by the following iterative formula:

St_1 = St_0(1 + rDt)+vol*sqrt(Dt)*Z_1

in which vol represent the volatility of the underlying asset and Z is the sample from a normal distribution.

## Newton Method

The Newton-Raphson method is a root-finding algorithm which produces successively better approximations to the zeroes of a function.
The general formulation is:

The algorithm start from an initial guess and proceed until a certain precision or the max number of iterations is reached.

In this project the algorithm return the best estimation for the implied volatility.

## Structure of the project
These are the steps in order to run the simulation:

1. First, the user has to choose the personal settings that want to implement in the model. The possible setting are:
     - S0, the initial price of the asset
     - R, the risk-free return
     - VOL, the volatility of the asset
     - TIME, the longest time for the simulation of the asset
     - STRIKE, the biggest value of strike for the simulation of the asset
     - t_int, the number of intervals of the expiration time
     - k_int, the number of different strikes in the range  
     - N_SIM, the number of the simulations of the underlying asset
     - N_INTER, the number in which the time will be divided for the Euler scheme simulation for the asset

2. Then, the user has to launch the vol.py file, that import its parameters from the configuration.txt file.

3. The output of the script are the surface of the generated prices and the implied volatility surface that will be saved as .png in the directory of the script.


The project are divided in different blocks:
- The configuration.txt file contains all the settable parameters for the model
- The func.py file contains all the defined functions used in the simulations
- The vol.py file contains the main part of the project in which all the defined function are recalled and in which the simulations are done

The script can be easily adapt to particular definition of volatility of the underlying asset, and the parameters can be set at will in the configuration.txt file.

Here are reported two sample image for the price and implied volatility surfaces.

![Price](https://user-images.githubusercontent.com/79851638/150512253-9290aa0c-680a-4824-888c-92f5361bf8e5.png)
![Vol](https://user-images.githubusercontent.com/79851638/150512261-33bc6a25-1a81-49e8-8972-0bddfd6177d4.png)


