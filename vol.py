import configparser
import numpy as np
import impl_func 

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

T_array = np.linspace(0.5, TIME, T_INT)
K_array = np.linspace(0.5, STRIKE, K_INT)

KK, TT = np.meshgrid(K_array,T_array)
CC = np.empty(shape=(T_INT,K_INT))
VV = np.empty(shape=(T_INT,K_INT))

np.random.seed(20000)

CC = price(T_array, K_array, N_INTER, N_SIM, S0, R, VOL, CC)

#for i in range(len(T_array)):
#    for j in range(len(K_array)):
#        VV[i,j] = find_imp_vol(CC[i,j], S=S0, K=K_array[j], T=T_array[i], r=R)

#print(VV)
