# Libraries
import matplotlib.pyplot as plt
import numpy as np

# Parameters

mu_max = 0.3     # (h^-1) maximum growth rate
Ks = 1           # (g/L) half saturation constant
Ki = 50          # (g/L) inhibition constant
m = 6            # constant
n = 1.5          # constant
Sm = 100         # (g/L) critical inhibitor concentration

S = np.arange(0, 100, 1)

# Monod:

mu1 = mu_max*S/(S+Ks)

# Haldane:
    
mu2 = mu_max*S/(Ks+S+(S*S/Ki))
   
# Han-Levenspiel:

mu3 = mu_max*((1-(S/Sm))**n)*(S/(S+Ks*((1-(S/Sm))**m)))

# mu vs S plot

plt.plot(S, mu1, color = 'magenta', linestyle='-', label='Monod')
plt.plot(S, mu2, color = 'blue', linestyle='-', label='Haldane')
plt.plot(S, mu3, color = 'green', linestyle='-', label='Han-Levenspiel')

plt.xlabel('Substrato S (g/L)', loc='center', fontsize=12)
plt.ylabel('\u03bc ($h^{-1}$)', loc='center', fontsize=12, labelpad=15)
plt.legend(loc='upper center', bbox_to_anchor=(0.8, 0.8), 
           frameon=False, ncol=1, fontsize=10)
