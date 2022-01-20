import configparser
from sys import argv

config = configparser.ConfigParser()
config.read(sys.argv[1])

S0 = config.get('settings', 'S0')
R = config.get('settings', 'R')
