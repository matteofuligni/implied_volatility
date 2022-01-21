import configparser
import numpy as np
import func


# Loading of settings
config = configparser.ConfigParser()
config.read('configuration.txt')
S0 = float(config.get('settings', 'S0'))
R = float(config.get('settings', 'R'))
VOL = float(config.get('settings', 'VOL'))
TIME = float(config.get('settings', 'TIME'))
STRIKE = float(config.get('settings', 'STRIKE'))
t_int = int(config.get('settings', 't_int'))
k_int = int(config.get('settings', 'k_int'))
N_SIM = int(config.get('settings', 'N_SIM'))
N_INTER = int(config.get('settings', 'N_INTER'))

T_array = np.linspace(0.5, TIME, t_int)
K_array = np.linspace(0.5, STRIKE, k_int)

KK, TT = np.meshgrid(K_array,T_array)
CC = np.empty(shape=(t_int,k_int))
VV = np.empty(shape=(t_int,k_int))

np.random.seed(20000)

CC = func.price(T_array, K_array, N_INTER, N_SIM, S0, R, VOL, CC)

print(CC)
