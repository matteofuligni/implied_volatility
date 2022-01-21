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

CC = func.price(T_array, K_array, N_INTER, N_SIM, S0, R, VOL, CC)

for i in range(len(T_array)):
    for j in range(len(K_array)):
        VV[i,j] = func.find_imp_vol(CC[i,j], S=S0, K=K_array[j], T=T_array[i], r=R)


# Price Chart
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

# Volatility Chart
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
