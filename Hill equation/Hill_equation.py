# Libraries
import numpy as np
from matplotlib import pyplot as plt

# Variable n ***********************************************************

S = np.linspace(0, 25, num=100)
Vmax = 12
Km = 10
n = [ 4, 6, 7, 3, 1, 0.5, 0.2 ]
V = np.empty([7,100])
for i in range(0,100):
    for j in range(0,7):
        V[j][i] = Vmax*(S[i]**n[j])/((Km**n[j])+(S[i]**n[j]))
        
# Define plot space
fig, axs = plt.subplots(1,3, figsize=(30,10))
fig.suptitle("Hill equation", fontsize =20, fontweight='bold')

# Data:
for j in range(0,7):
    axs[0].plot(S, V[j][:], linestyle='-', label='n={}'.format(n[j]))

axs[0].set_xlabel('S', loc='center', fontsize=15)
axs[0].set_ylabel('V', loc='center', fontsize=15, labelpad=15)
axs[0].legend(loc='upper center', bbox_to_anchor=(0.2, 0.9), 
           frameon=False, ncol=1, fontsize=15)

axs[0].text(0.5, 6, 'Negative cooperation')
axs[0].text(8, 1, 'Positive cooperation')
axs[0].text(2.5, 2, 'No cooperation', rotation=50)


# Variable Vmax ***********************************************************

S = np.linspace(0, 25, num=100)
Vmax = [0.1, 2, 4, 6, 8, 10]
Km = 10
n = 4
V = np.empty([7,100])
for i in range(0,100):
    for j in range(0,6):
        V[j][i] = Vmax[j]*(S[i]**n)/((Km**n)+(S[i]**n))
        
# Data:
for j in range(0,6):
    axs[1].plot(S, V[j][:], linestyle='-', label='Vmax={}'.format(Vmax[j]))

axs[1].set_xlabel('S', loc='center', fontsize=15)
axs[1].set_ylabel('V', loc='center', fontsize=15, labelpad=15)
axs[1].legend(loc='upper center', bbox_to_anchor=(0.2, 0.9), 
           frameon=False, ncol=1, fontsize=15)


# Variable Km ***********************************************************


S = np.linspace(0, 25, num=100)
Vmax = 12
Km = [0.1, 2, 4, 6, 8, 10]
n = 4
V = np.empty([7,100])
for i in range(0,100):
    for j in range(0,6):
        V[j][i] = Vmax*(S[i]**n)/((Km[j]**n)+(S[i]**n))
        
# Data:
for j in range(0,6):
    axs[2].plot(S, V[j][:], linestyle='-', label='Vmax={}'.format(Km[j]))

axs[2].set_xlabel('S', loc='center', fontsize=15)
axs[2].set_ylabel('V', loc='center', fontsize=15, labelpad=15)
axs[2].legend(loc='upper center', bbox_to_anchor=(0.8, 0.5), 
           frameon=False, ncol=1, fontsize=15)
