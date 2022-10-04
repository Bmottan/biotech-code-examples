# Libraries
import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import solve_ivp

# System Model Function
def dy(t,y):
    #**********************************************
    # Variables:
    #   y[0] : XV
    #   y[1] : SV
    #   y[2] : PV
    #   y[3] : V
    #**********************************************
    S = y[1]/y[3]    # (g/L) substrate at reactor
    Fe = 1           # (L/h) feed rate entry
    F = Fe           # (L/h) feed rate exit
    # Cells (X)
    Xe = 0           # (g/L) cells at feed
    mu_max = 0.3     # (h^-1) 
    Ks = 1           # (g/L)
    mu = mu_max*S/(S+Ks) # (h^-1) specific growth rate - Monod
    kd = 0           #(1/h) cell death constant - negligible -
    # Substrate (S)
    Se = 50          # (g/L) substrate at feed
    Yxs = 0.5        # (g_cell/g_sub) cell yield
    mu_s = mu/Yxs    # (g_sub/g_cell.h) specific consumption rate
    # Product (P)
    Pe = 0           # (g/L) product at feed
    Yps = 0.25       # (g_prod/g_sub) prod yield
    mu_p = mu/Yps    # (g_sub/g_prod.h) specific production rate
    kdp = 0          # (1/h) product degradation constant - negligible - 
    #**********************************************
    dy = [0,0,0,0]
    dy[0] = Fe*Xe-F*y[0]/y[3]+mu*y[0]-kd*y[0]
    dy[1] = Fe*Se-F*y[1]/y[3]-mu_s*y[0]
    dy[2] = Fe*Pe-F*y[2]/y[3]+mu_p*y[0]-kdp*y[2]
    dy[3] = Fe-F
    return dy


#**********************************************
# Simple Reactor
#********************************************
# Initializations
#********************************************
XV0 = 0.5   # (g) initial cells
SV0 = 500   # (g) initial substrate
PV0 = 0     # (g) initial product
V0 = 10     # (L) initial reactor volume
tf = 30     # (h) time frame
y0 = [XV0, SV0, PV0, V0]
tspan = [0, 30]
teval = np.arange(0, tspan[1], 0.1)

#********************************************
# Solve ODE Equations
#********************************************
sol = solve_ivp(dy, tspan, y0, method = 'RK45', t_eval=teval);
 
XV = sol.y[0]
SV = sol.y[1]
PV = sol.y[2]
V = sol.y[3]
X=[]; S=[]; P=[]
for i in range(len(sol.y[0])):
    X.append(XV[i]/V[i])
    S.append(SV[i]/V[i])
    P.append(PV[i]/V[i])


#**********************************************
# Plot results
#**********************************************

# Define plot space
fig, ax1 = plt.subplots(figsize=(10,10))
fig.suptitle("Simulação de Reator: CSTR", fontsize =20, fontweight='bold')

# Data: Substrate
ax1.plot(sol.t, S, color = 'magenta', linestyle='-', label='S (g/L)')

# Data: Biomass
ax2 = ax1.twinx()
ax2.plot(sol.t, X, color = 'blue', linestyle='-', label='X (g/L)')

# Data: Product
ax2.plot(sol.t, P, color = 'red', linestyle='-', label='P (g/L)')

# Data: Volume
ax2.plot(sol.t, V, color = 'gray', linestyle='-', label='V (L)')

# Labels and format
ax1.set_xlabel('Tempo (h)', loc='center', fontsize=15)
ax1.set_ylabel('Substrato S (g/L)', loc='center', fontsize=15, labelpad=15)
ax1.legend(loc='upper center', bbox_to_anchor=(0.2, 0.9), 
           frameon=False, ncol=1, fontsize=15)
ax2.set_ylabel('Biomassa X (g/L),   Produto P (g/L),   Volume V (L)',
               loc='center', fontsize=15, labelpad=15)
ax2.legend(loc='upper center', bbox_to_anchor=(0.2, 0.86), 
           frameon=False, ncol=1, fontsize=15)

#**********************************************