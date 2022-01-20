import configparser


config = configparser.ConfigParser()
config.read('configuration.txt')

S0 = config.get('settings', 'S0')
R = config.get('settings', 'R')
