import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib import cm
from time import time

def sigma(S, VOL):
    """ This method compute the value of the volatility in the case
        it depends on the price.

        Parameters
            S : the assets price

        Returns
            The value of the volatility """
    vol = VOL # A possible alternative could be: np.multiply(.2*np.maximum(1,2-S),S)
    return vol

def price(T_array, K_array, N_INTER, N_SIM, S0, R, VOL):
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
    t0 = time()
    CC = np.zeros(shape=(len(T_array),len(K_array)))
    norm = stats.norm.rvs(size=(N_INTER,N_SIM))
    print('Normal Generated! Time: ', round(time()-t0, 2))
    r=R; sim=N_SIM; inter=N_INTER;
    for i in range(len(T_array)):
        T = T_array[i]; dt = T/inter; att=np.exp(-r*T)
        for g in range(len(K_array)):
            k=K_array[g]
            S = np.empty((sim)); S.fill(S0)
            V = np.empty((sim)); V.fill(sigma(S0, VOL))
            for j in range(inter):
                dw = np.sqrt(dt)*norm[j,:]
                V = sigma(S, VOL) # The vol can be set as a func of the underlying asset
                S = S*(1+r*dt)+np.multiply(V,dw)
            payoff = np.maximum(S-k,0).mean()
            CC[i,g] = payoff*att
            tnp2 = time() - t0
            print('Done : C[', i, ']','[',g,']', 'Time: ', round(tnp2,2))
    print(CC)
    return CC


def bs_call(S, K, T, r, vol):
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
    out = 0
    with np.errstate(divide='ignore', invalid='ignore'):
        d1 = np.nan_to_num(np.divide((np.log(S/K) + (r + 0.5*vol**2)*T),(vol*np.sqrt(T))))
        d2 = d1 - vol * np.sqrt(T)
        out = S * stats.norm.cdf(d1) - np.exp(-r * T) * K * stats.norm.cdf(d2)
        if out == np.nan:
            return 0.0
    return out


def bs_vega(S, K, T, r, sigma):
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
    out = 0
    with np.errstate(divide='ignore', invalid='ignore'):
        d1 = np.divide((np.log(S / K) + (r + 0.5 * sigma ** 2) * T),(sigma * np.sqrt(T)))
        out = S * stats.norm.pdf(d1) * np.sqrt(T)
    return out


def find_imp_vol(target_value, S, K, T, r):
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
    MAX_ITERATIONS = 100000
    PRECISION = 1.0e-8
    _sigma = 0.3
    for i in range(0, MAX_ITERATIONS):
        price = bs_call(S, K, T, r, _sigma)
        vega = bs_vega(S, K, T, r, _sigma)
        diff = target_value - price
        if (abs(diff) < PRECISION):
            return np.float64(_sigma)
        _sigma = _sigma + np.divide(diff,vega)
    print('Sigma not found')
    return _sigma



def price_chart(KK, TT, CC):
    """ This method plot the price chart.

        Parameters
            KK : the strike meshgrid
            TT : the time meshgrid
            CC : the price matrix
        """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(KK, TT, CC, facecolors=cm.jet(CC), lw=0)
    plt.locator_params(axis="x", nbins=5)
    plt.locator_params(axis="y", nbins=5)
    plt.locator_params(axis="z", nbins=5)
    ax.set_xlabel('Strike', fontsize='14')
    ax.set_ylabel('Time', fontsize='14')
    ax.set_zlabel('Price', fontsize='14')
    ax.tick_params(axis='both', which='major', labelsize=10)
    plt.title('Price Chart', fontsize='24')
    plt.savefig('Price.png', dpi = 300)
    plt.show()

def volatility_chart(KK, TT, VV):
    """ This method plot the implied volatility chart.

        Parameters
            KK : the strike meshgrid
            TT : the time meshgrid
            VV : the implied volatility matrix
        """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(KK, TT, VV, facecolors=cm.jet(VV), lw=0)
    plt.locator_params(axis="x", nbins=5)
    plt.locator_params(axis="y", nbins=5)
    plt.locator_params(axis="z", nbins=5)
    ax.set_xlabel('Strike', fontsize='14')
    ax.set_ylabel('Time', fontsize='14')
    ax.set_zlabel('Vol', fontsize='14')
    ax.tick_params(axis='both', which='major', labelsize=10)
    plt.title(' Volatility Chart', fontsize='24')
    plt.savefig('Vol.png', dpi = 300)
    plt.show()
