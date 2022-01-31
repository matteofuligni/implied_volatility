# Implied Volatility Surface

## Summary
With this script its possible to generate the implied volatility surface for a defined option with the Euler and Monte Carlo methods.

The implied volatility is the volatility as if that price obtained of an option was calculated with the Black-Scholes model.
The Black-Scholes formula for a call (that is one of the vanilla option) is the following:

<img src="https://latex.codecogs.com/png.image?\dpi{110}&space;C&space;=&space;S_tN(d_1)&space;-&space;Ke^{-rt}N(d_2)" title="C = S_tN(d_1) - Ke^{-rt}N(d_2)" />

Where:

<img src="https://latex.codecogs.com/png.image?\dpi{110}&space;d_1&space;=&space;\frac{\ln{\frac{S_t}{K}}&plus;(r&plus;\frac{\sigma^2_{\nu}}{2})t}{\sigma_s\sqrt{t}" title="d_1 = \frac{\ln{\frac{S_t}{K}}+(r+\frac{\sigma^2_{\nu}}{2})t}{\sigma_s\sqrt{t}" />

and

<img src="https://latex.codecogs.com/png.image?\dpi{110}&space;d_1&space;=&space;\frac{\ln{\frac{S_t}{K}}&plus;(r&plus;\frac{\sigma^2_{\nu}}{2})t}{\sigma_s\sqrt{t}" title="d_1 = \frac{\ln{\frac{S_t}{K}}+(r+\frac{\sigma^2_{\nu}}{2})t}{\sigma_s\sqrt{t}" />

The implied volatility surface represent one of the best way to evaluate an option in finance.

## Monte Carlo Method
Monte Carlo Method is a simple technique of numerical approximation of the mean of a random variable X. It is used in many circumstances in mathematica finance and in particular in the pricing problem.

Generally speaking Monte Carlo Method allows approximating the value of an integral numerically. If Y is uniformly distributed on [0,1] and X = f(Y), then the expectation value of X is

<img src="https://latex.codecogs.com/png.image?\dpi{110}&space;E[x]&space;=&space;\int&space;f(x)dx" title="E[x] = \int f(x)dx" />

The expectation value of X is the best estimation of the X mean.

This method is used in this project to estimate the prices of an option.

## Euler Method
This method is used here to numerically approximate a stochastic differential equation that regulate the being of an underlying asset.

The Euler scheme implemented in the script are represented by the following iterative formula:

<img src="https://latex.codecogs.com/png.image?\dpi{110}&space;St_1&space;=&space;St_0&space;(1&plus;r\Delta&space;t)&plus;\sigma&space;*\sqrt{\Delta&space;t}*Z_1" title="St_1 = St_0 (1+r\Delta t)+\sigma *\sqrt{\Delta t}*Z_1" />

in which vol represent the volatility of the underlying asset and Z is the sample from a normal distribution.

## Newton Method

The Newton-Raphson method is a root-finding algorithm which produces successively better approximations to the zeroes of a function.
The general formulation is:

<img src="https://latex.codecogs.com/png.image?\dpi{110}&space;x_{n&plus;1}&space;=&space;x_n&space;-\frac{f(x_n)}{f'(x_n)}" title="x_{n+1} = x_n -\frac{f(x_n)}{f'(x_n)}" />

The algorithm start from an initial guess and proceed until a certain precision or the max number of iterations is reached.

In this project the algorithm return the best estimation for the implied volatility.

## Structure of the project
These are the steps in order to run the simulation:

1. First, the user has to choose the personal settings that want to implement in the model through the configuration.txt file. The possible setting are:
     - R, the risk-free return (usually small positive < 0.1)
     - VOL, the volatility of the asset (usually 0 < Vol < 1)

2. There are also other parameters in model that can be defied in some ways "standard", that can be set at will. I suggest to leave them as they are, because are in the optimal way to analyze this type of implied volatility problem. They are:
     - S0 = 1, the initial price of the asset
     - TIME = 2, the longest time for the simulation of the asset in years
     - STRIKE = 1.5, the biggest value of strike for the simulation of the asset
     - t_int = 10, the number of intervals of the expiration time
     - k_int = 10, the number of different strikes in the range  
     - N_SIM = 10000, the number of the simulations of the underlying asset
     - N_INTER = 10000, the number in which the time will be divided for the Euler scheme simulation for the asset

3. Then, the user has to launch the vol.py file, that import its parameters from the configuration.txt file.

4. The output of the script are the surface of the generated prices and the implied volatility surface that will be saved as .png in the directory of the script.


The project are divided in different blocks:
- The configuration.txt file contains all the settable parameters for the model
- The func.py file contains all the defined functions used in the simulations
- The vol.py file contains the main part of the project in which all the defined function are recalled and in which the simulations are done

The script can be easily adapt to particular definition of volatility of the underlying asset, and the parameters can be set at will in the configuration.txt file.

Here are reported two sample image for the price and implied volatility surface.

![Price](https://user-images.githubusercontent.com/79851638/150512253-9290aa0c-680a-4824-888c-92f5361bf8e5.png)
![Vol](https://user-images.githubusercontent.com/79851638/150512261-33bc6a25-1a81-49e8-8972-0bddfd6177d4.png)
