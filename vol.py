import configparser
import numpy as np
import func
from time import time

# Loading of settings
config = configparser.ConfigParser()
config.read('configuration.txt')
S0 = float(config.get('settings', 'S0'))
R = float(config.get('settings', 'R'))
VOL = float(config.get('settings', 'VOL'))
TIME = float(config.get('settings', 'TIME'))
STRIKE = float(config.get('settings', 'STRIKE'))
T_INT = int(config.get('settings', 'T_INT'))
K_INT = int(config.get('settings', 'K_INT'))
N_SIM = int(config.get('settings', 'N_SIM'))
N_INTER = int(config.get('settings', 'N_INTER'))

# Create the array for strike and time
T_array = np.linspace(0.5, TIME, T_INT)
K_array = np.linspace(0.5, STRIKE, K_INT)

# Create the meshgrid
KK, TT = np.meshgrid(K_array,T_array)
CC = np.empty(shape=(T_INT,K_INT))
VV = np.empty(shape=(T_INT,K_INT))

# Set the random seed
np.random.seed(20000)

# Fix the zero time
t0 = time()

# Compute the price matrix
CC = func.price(T_array, K_array, N_INTER, N_SIM, S0, R, VOL, CC)

# Find the implied volatility matrix
for i in range(len(T_array)):
    for j in range(len(K_array)):
        VV[i,j] = func.find_imp_vol(CC[i,j], S=S0, K=K_array[j], T=T_array[i], r=R)

# Total time
print('All Done! Time: ', round(time()-t0, 2))

# Price Chart
func.price_chart(KK, TT, CC)
# Volatility Chart
func.volatility_chart(KK, TT, VV)
