import configparser
import numpy as np


# Loading of settings
config = configparser.ConfigParser()
config.read('configuration.txt')

S0 = config.get('settings', 'S0')
R = config.get('settings', 'R')
VOL = config.get('settings', 'VOL')
t_int = config.get('settings', 't_int')
k_int = config.get('settings', 'k_int')
N_SIM = config.get('settings', 'N_SIM')
N_INTER = config.get('settings', 'N_INTER')
