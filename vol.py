import configparser
import numpy as np
import func


# Loading of settings
config = configparser.ConfigParser()
config.read('configuration.txt')
S0 = config.get('settings', 'S0')
R = config.get('settings', 'R')
VOL = config.get('settings', 'VOL')
TIME = config.get('settings', 'TIME')
STRIKE = config.get('settings', 'STRIKE')
t_int = config.get('settings', 't_int')
k_int = config.get('settings', 'k_int')
N_SIM = config.get('settings', 'N_SIM')
N_INTER = config.get('settings', 'N_INTER')

T_array = np.linspace(0.5, TIME, t_int)
K_array = np.linspace(0.5, STRIKE, k_int)

KK, TT = np.meshgrid(K_array,T_array)
CC = np.empty(shape=(t_int,k_int))
VV = np.empty(shape=(t_int,k_int))
