import numpy as np

def sigma(S):
    """ This method compute the value of the volatility in the case
        it depends on the price.

        Parameters
            S : the assets price

        Returns
            The value of the volatility """
    sigma = VOL #np.multiply(.2*np.maximum(1,2-S),S)
    return sigma

def price(T_array, K_array, N_INTER):
    """ This method implement the Monte Carlo and Euler methods to compute
        the expectation value of all the prices by varying the
        expiration time and the strike.

        Parameters
            T_array : an array with all the possible expiration times
            K_array : an array with all the possible strike
            N_INTER : the number of interval in which the trajectory
                      of the underlying asset has been divided to
                      implement the Euler scheme

        Returns
            A matrix with all the computed prices
    """
    r=R; sim=N_SIM; inter=N_INTER;
    for i in range(len(T_array)):
        T = T_array[i]; dt = T/inter; att=np.exp(-r*T)
        for g in range(len(K_array)):
            k=K_array[g]
            S = np.empty((sim)); S.fill(S0)
            V = np.empty((sim)); V.fill(sigma(S0))
            for j in range(inter):
                dw = np.sqrt(dt)*norm[j,:]
                V = sigma(S) # The vol can be set as a func of the underlying asset
                S = S*(1+r*dt)+np.multiply(V,dw)
            payoff = np.maximum(S-k,0).mean()
            CC[i,g] = payoff*att
    return CC
