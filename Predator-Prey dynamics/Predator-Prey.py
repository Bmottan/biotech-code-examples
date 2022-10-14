# Libraries
import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import solve_ivp


#******************************************************************************
# Simplified model for Predator-Prey system
#******************************************************************************

# Replicate Figure 2 Oscillations
# Parameters ******************************************************************

kc1 = 0.8 #specific growth rate for 1 (h^-1)
kc2 = 0.4 #specific growth rate for 2(h^-1)
cmax = 100 #carrying capacity for cell growth (10^3 cells/nL)
beta = 2 #Cooperativity of AHL effect
kA1 = 0.1 # AHL 1 synthesis rate (nM.mL/h)
d_Ae1 = 0.017 # AHL 1 extracellular decay rate constant (h^-1)
d_Ae2 = 0.11 # AHL 2 extracellular decay rate constant (h^-1)
D = 0.1125 # dilution rate (h^-1)
K1 = 10 #Concentration of AHL necessary to half max activity of PluxI promoter (nM)
K2 = K1 #Concentration of AHL necessary to half max activity of PluxI promoter (nM)
IPTG = [0,5,1000] #IPTG concentration (uM)
dc2 = 0.3 # death rate for 2 (h^-1)

# ODEs ************************************************************************
def PredPray(t,C,kc1,kc2,cmax,beta,dc1,dc2,K1,K2,kA1,kA2,d_Ae1,d_Ae2,D):
    #******************************************************************
    #   C[0] = C1  --- Predator (MG1655) (cells/mL)(min^-1)
    #   C[1] = C2  --- Prey (Top10F') (cells/mL)(min^-1)
    #   C[2] = Ae1 --- AHL 1 in the medium (3OC12HSL) (nM)(min^-1)
    #   C[3] = Ae2 --- AHL 2 in the medium (3OC6HSL) (nM)(min^-1)
    #******************************************************************

    dC = [0,0,0,0]

    dC[0] = kc1*C[0]*(1-((C[0]+C[1])/cmax))-(dc1*C[0]*K1/(K1+(C[3]**beta)))-D*C[0]
    dC[1] = kc2*C[1]*(1-((C[0]+C[1])/cmax))-(dc2*C[1]*(C[2]**beta)/(K2+(C[2]**beta)))-D*C[1]
    dC[2] = kA1*C[0]-(d_Ae1+D)*C[2]
    dC[3] = kA2*C[1]-(d_Ae2+D)*C[3]
    
    return dC


# Plot ODEs *******************************************************************
plt.style.use(r'C:\Users\bruno\OneDrive\Documentos\GitHub\biotech-code-examples\style_preset\plot_preset.mplstyle')

fig1, axs = plt.subplots(2,3, figsize=(30, 15))

for i in range(0,3):
    dc1 = 0.5+1*(IPTG[i]**2)/(25+IPTG[i]**2); # death rate for 1 (h^-1)
    kA2 = 0.02 + 0.03*(IPTG[i]**2)/(25+IPTG[i]**2); # AHL 2 synthesis rate (nM.mL/h)
    
    # ODEs for cells and AHL ********************************************
        
    C0 = [20, 20, 0, 0] #initial concentrations (cells/nL , cells/nL , nM , nM)
    tspan = [0, 400] # time span (h)
    teval = np.arange(0, tspan[1]+1, 1) 

    #********************************************
    # Solve ODE Equations
    #********************************************
    sol = solve_ivp(lambda t,C: PredPray(t,C,kc1,kc2,cmax,beta,dc1,dc2,K1,K2,kA1,kA2,d_Ae1,d_Ae2,D), tspan, C0, method = 'RK45', t_eval=teval)
      
   
    axs[0,i].set_title('IPTG = {} $\mu M$'.format(IPTG[i]), fontsize=15, fontweight='bold')
    axs[0,i].plot(sol.t, sol.y[0], label='Predator')
    axs[0,i].plot(sol.t, sol.y[1], label='Prey')
    axs[0,i].set_xlabel('t (h)')
    axs[0,i].set_ylabel('Cell Number ($x10^{3}$ cells/nL)')
    axs[0,i].legend(loc='upper center', bbox_to_anchor=(0.8, 0.9), 
                    frameon=True, ncol=1, fontsize=15)
    
        
    axs[1,i].set_title('IPTG = {} $\mu M$'.format(IPTG[i]), fontsize=15, fontweight='bold')
    axs[1,i].plot(sol.t, sol.y[2], label='AHL 1')
    axs[1,i].plot(sol.t, sol.y[3], label='AHL 2')
    axs[1,i].set_xlabel('t (h)')
    axs[1,i].set_ylabel('Concentration (nM)')
    axs[1,i].legend(loc='upper center', bbox_to_anchor=(0.8, 0.9), 
                    frameon=True, ncol=1, fontsize=15)
    
    
#%%
# Libraries
import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import solve_ivp
import mpl_toolkits.axes_grid1.inset_locator as il

# Bifurcation Predator Growth x Death
# Parameters ******************************************************************

k_c1 = np.arange(0, 2+.02, 0.02) #specific growth rate for 1 (h^-1)
kc2 = 0.4 #specific growth rate for 2(h^-1)
cmax = 100 #carrying capacity for cell growth (10^3 cells/nL)
beta = 2 #Cooperativity of AHL effect
kA1 = 0.1 # AHL 1 synthesis rate (nM.mL/h)
d_Ae1 = 0.017 # AHL 1 extracellular decay rate constant (h^-1)
d_Ae2 = 0.11 # AHL 2 extracellular decay rate constant (h^-1)
D = 0.1125 # dilution rate (h^-1)
K1 = 10 #Concentration of AHL necessary to half max activity of PluxI promoter (nM)
K2 = K1 #Concentration of AHL necessary to half max activity of PluxI promoter (nM)
IPTG = 5 #IPTG concentration (uM)
dc2 = 0.3 # death rate for 2 (h^-1)
d_c1 = np.arange(0, 2+.02, 0.02); # death rate for 1 (h^-1)
kA2 = 0.02 + 0.03*(IPTG**2)/(25+IPTG**2); # AHL 2 synthesis rate (nM.mL/h)


# ODEs ************************************************************************
def PredPray(t,C,kc1,kc2,cmax,beta,dc1,dc2,K1,K2,kA1,kA2,d_Ae1,d_Ae2,D):
    #******************************************************************
    #   C[0] = C1  --- Predator (MG1655) (cells/mL)(min^-1)
    #   C[1] = C2  --- Prey (Top10F') (cells/mL)(min^-1)
    #   C[2] = Ae1 --- AHL 1 in the medium (3OC12HSL) (nM)(min^-1)
    #   C[3] = Ae2 --- AHL 2 in the medium (3OC6HSL) (nM)(min^-1)
    #******************************************************************

    dC = [0,0,0,0]

    dC[0] = kc1*C[0]*(1-((C[0]+C[1])/cmax))-(dc1*C[0]*K1/(K1+(C[3]**beta)))-D*C[0]
    dC[1] = kc2*C[1]*(1-((C[0]+C[1])/cmax))-(dc2*C[1]*(C[2]**beta)/(K2+(C[2]**beta)))-D*C[1]
    dC[2] = kA1*C[0]-(d_Ae1+D)*C[2]
    dC[3] = kA2*C[1]-(d_Ae2+D)*C[3]
    
    return dC

# Oscillatory behavior vs Prey domination vs Predator domination

# Solve ODEs ******************************************************************

monostable_predator=[]
monostable_prey=[]
bistable=[]

for i in range(0,100): #column
    for j in range(0,100): #row
    
        kc1=k_c1[i]
        dc1=d_c1[j]
    
        #********************************************
        # Solve ODE Equations for cells and AHL
        #********************************************
        C0 = [20, 20, 0, 0] #initial concentrations (cells/nL , cells/nL , nM , nM)
        tspan = [0, 400] # time span (h)
        teval = np.arange(0, tspan[1]+1, 1)    
        sol = solve_ivp(lambda t,C: PredPray(t,C,kc1,kc2,cmax,beta,dc1,dc2,K1,K2,kA1,kA2,d_Ae1,d_Ae2,D), tspan, C0, method = 'RK45', t_eval=teval)
     
        # Diff of pred-prey cell population
        diff = []
        for k in range(0,len(sol.y[0])):
            sort = sol.y[0,k]-sol.y[1,k]
            if sort > 0:
                sort = 1 #pred
            else:
                sort = 2 #prey
            diff = np.append(diff, sort)
    
        for o in range(100,len(diff)): # eval stability after 100h

            if sum(diff[100:]) == 1*(len(diff)-100):
                monostable_predator.append((kc1,dc1))
            elif sum(diff[100:]) == 2*(len(diff)-100):
                monostable_prey.append((kc1,dc1))
            else:
                bistable.append((kc1,dc1))

    print('{}%'.format(i)) # Progress


# Plot
plt.style.use(r'C:\Users\bruno\OneDrive\Documentos\GitHub\biotech-code-examples\style_preset\plot_preset.mplstyle')

fig2, axs = plt.subplots(1,1, figsize=(10,10))

axs.scatter(*zip(*monostable_predator), marker="s", s=100, label='Predator domination')
axs.scatter(*zip(*monostable_prey), marker="s", s=100, label='Prey domination')
axs.scatter(*zip(*bistable), marker="s", s=100, label='Oscillatory behavior')
axs.set_xlabel('kc1 ($h^{-1}$)')
axs.set_ylabel('dc1 ($h^{-1}$)')
axs.set_title('Bifurcation plot for predator \n growth vs death rates')

axs.text(x=0.2, y=0.8, s="Prey domination", 
        transform=fig2.transFigure, ha='left', fontsize=18)
axs.text(x=0.6, y=0.8, s="Oscillatory behavior", 
        transform=fig2.transFigure, ha='left', fontsize=18)
axs.text(x=0.6, y=0.35, s="Predator domination", 
        transform=fig2.transFigure, ha='left', fontsize=18)

# Add inset plot on diff regions:
## mono pred *******************************************************************
kc1=1.75
dc1=0.25
# ODEs for cells and AHL    
C0 = [20, 20, 0, 0] #initial concentrations (cells/nL , cells/nL , nM , nM)
tspan = [0, 400] # time span (h)
teval = np.arange(0, tspan[1]+1, 1) 
sol = solve_ivp(lambda t,C: PredPray(t,C,kc1,kc2,cmax,beta,dc1,dc2,K1,K2,kA1,kA2,d_Ae1,d_Ae2,D), tspan, C0, method = 'RK45', t_eval=teval)
axins = il.inset_axes(axs, "30%", "30%", loc='lower left', borderpad=0,
    bbox_to_anchor=(0.6,0.15,0.7,0.4),bbox_transform=axs.transAxes)
axins.plot(sol.t, sol.y[0], label='Predator')
axins.plot(sol.t, sol.y[1], label='Prey')
axins.set_xlabel('Time')
axins.set_ylabel('Cells')
## mono prey *******************************************************************
kc1=0.25
dc1=1.5
# ODEs for cells and AHL    
C0 = [20, 20, 0, 0] #initial concentrations (cells/nL , cells/nL , nM , nM)
tspan = [0, 400] # time span (h)
teval = np.arange(0, tspan[1]+1, 1) 
sol = solve_ivp(lambda t,C: PredPray(t,C,kc1,kc2,cmax,beta,dc1,dc2,K1,K2,kA1,kA2,d_Ae1,d_Ae2,D), tspan, C0, method = 'RK45', t_eval=teval)
axins = il.inset_axes(axs, "30%", "30%", loc='lower left', borderpad=0,
    bbox_to_anchor=(0.15,0.7,0.7,0.4),bbox_transform=axs.transAxes)
axins.plot(sol.t, sol.y[0], label='Predator')
axins.plot(sol.t, sol.y[1], label='Prey')
axins.set_xlabel('Time')
axins.set_ylabel('Cells')
## bistable ********************************************************************
kc1=1.25
dc1=1.5
# ODEs for cells and AHL    
C0 = [20, 20, 0, 0] #initial concentrations (cells/nL , cells/nL , nM , nM)
tspan = [0, 400] # time span (h)
teval = np.arange(0, tspan[1]+1, 1) 
sol = solve_ivp(lambda t,C: PredPray(t,C,kc1,kc2,cmax,beta,dc1,dc2,K1,K2,kA1,kA2,d_Ae1,d_Ae2,D), tspan, C0, method = 'RK45', t_eval=teval)
axins = il.inset_axes(axs, "30%", "30%", loc='lower left', borderpad=0,
    bbox_to_anchor=(0.55,0.7,0.7,0.4),bbox_transform=axs.transAxes)
axins.plot(sol.t, sol.y[0], label='Predator')
axins.plot(sol.t, sol.y[1], label='Prey')
axins.set_xlabel('Time')
axins.set_ylabel('Cells')



#%%
# Libraries
import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import solve_ivp
import mpl_toolkits.axes_grid1.inset_locator as il
from matplotlib import ticker as mticker

# Bifurcation Dilution x IPTG
# Parameters ******************************************************************

kc1 = 0.8 #specific growth rate for 1 (h^-1)
kc2 = 0.4 #specific growth rate for 2(h^-1)
cmax = 100 #carrying capacity for cell growth (10^3 cells/nL)
beta = 2 #Cooperativity of AHL effect
kA1 = 0.1 # AHL 1 synthesis rate (nM.mL/h)
d_Ae1 = 0.017 # AHL 1 extracellular decay rate constant (h^-1)
d_Ae2 = 0.11 # AHL 2 extracellular decay rate constant (h^-1)
Dil = np.linspace(0, 0.2, num=100) # dilution rate 0-0.2(h^-1)
K1 = 10 #Concentration of AHL necessary to half max activity of PluxI promoter (nM)
K2 = K1 #Concentration of AHL necessary to half max activity of PluxI promoter (nM)
IPTG = np.logspace(0, 3, num=100) #IPTG concentration 0-1000(uM)
dc2 = 0.3 # death rate for 2 (h^-1)

# ODEs ************************************************************************
def PredPray(t,C,kc1,kc2,cmax,beta,dc1,dc2,K1,K2,kA1,kA2,d_Ae1,d_Ae2,D):
    #******************************************************************
    #   C[0] = C1  --- Predator (MG1655) (cells/mL)(min^-1)
    #   C[1] = C2  --- Prey (Top10F') (cells/mL)(min^-1)
    #   C[2] = Ae1 --- AHL 1 in the medium (3OC12HSL) (nM)(min^-1)
    #   C[3] = Ae2 --- AHL 2 in the medium (3OC6HSL) (nM)(min^-1)
    #******************************************************************

    dC = [0,0,0,0]

    dC[0] = kc1*C[0]*(1-((C[0]+C[1])/cmax))-(dc1*C[0]*K1/(K1+(C[3]**beta)))-D*C[0]
    dC[1] = kc2*C[1]*(1-((C[0]+C[1])/cmax))-(dc2*C[1]*(C[2]**beta)/(K2+(C[2]**beta)))-D*C[1]
    dC[2] = kA1*C[0]-(d_Ae1+D)*C[2]
    dC[3] = kA2*C[1]-(d_Ae2+D)*C[3]
    
    return dC

# Solve ODEs ******************************************************************

monostable_predator=[]
monostable_prey=[]
bistable=[]

for i in range(0,100): #column (D)
    for j in range(0,100): #row (IPTG)
    
        dc1 = 0.5 + 1*(IPTG[j]**2)/(25+IPTG[j]**2) # death rate for 1 (h^-1)
        kA2 = 0.02 + 0.03*(IPTG[j]**2)/(25+IPTG[j]**2) # AHL 2 synthesis rate (nM.mL/h)
        D=Dil[i]
    
        #********************************************
        # Solve ODE Equations for cells and AHL
        #********************************************
        C0 = [20, 20, 0, 0] #initial concentrations (cells/nL , cells/nL , nM , nM)
        tspan = [0, 1000] # time span (h)
        teval = np.arange(0, tspan[1]+1, 1)    
        sol = solve_ivp(lambda t,C: PredPray(t,C,kc1,kc2,cmax,beta,dc1,dc2,K1,K2,kA1,kA2,d_Ae1,d_Ae2,D), tspan, C0, method = 'RK45', t_eval=teval)
     
        # Diff of pred-prey cell population
        diff = []
        for k in range(0,len(sol.y[0])):
            sort = sol.y[0,k]-sol.y[1,k]
            if sort > 0:
                sort = 1 #pred
            else:
                sort = 2 #prey
            diff = np.append(diff, sort)
    
        for o in range(100,len(diff)): # eval stability after 100h

            if sum(diff[100:]) == 1*(len(diff)-100):
                monostable_predator.append((D,IPTG[j]))
            elif sum(diff[100:]) == 2*(len(diff)-100):
                monostable_prey.append((D,IPTG[j]))
            else:
                bistable.append((D,IPTG[j]))

    print('{}%'.format(i)) # Progress


# Plot
plt.style.use(r'C:\Users\bruno\OneDrive\Documentos\GitHub\biotech-code-examples\style_preset\plot_preset.mplstyle')

fig3, axs = plt.subplots(1,1, figsize=(10,10))

axs.scatter(*zip(*monostable_predator), marker="s", s=100, label='Predator domination')
axs.scatter(*zip(*monostable_prey), marker="s", s=100, label='Prey domination')
axs.scatter(*zip(*bistable), marker="s", s=100, label='Oscillatory behavior')
axs.set_xlabel('D ($h^{-1}$)')
axs.set_ylabel('IPTG ($\mu M}$)')
axs.set_yscale('log')
axs.set_title('Bifurcation plot for \n dilution rates vs IPTG concentrations')
# Log scale minor ticks
axs.minorticks_on()
axs.tick_params(axis='y', which='minor', length=3)

axs.text(x=0.75, y=0.75, s="Prey \n"+"domination", 
        transform=fig3.transFigure, ha='left', fontsize=18)
axs.text(x=0.2, y=0.8, s="Oscillatory behavior", 
        transform=fig3.transFigure, ha='left', fontsize=18)
axs.text(x=0.15, y=0.12, s="Predator domination", 
        transform=fig3.transFigure, ha='left', fontsize=18)
axs.arrow(x=0.02, y=1.5, dx=0.01, dy=1, color='k', head_length=0.2, head_width=0.005)

# Add inset plot on diff regions:
## mono pred *******************************************************************
dc1 = 0.5 + 1*(2**2)/(25+2**2) # death rate for 1 (h^-1)
kA2 = 0.02 + 0.03*(2**2)/(25+2**2) # AHL 2 synthesis rate (nM.mL/h)
D=0.025
# ODEs for cells and AHL    
C0 = [20, 20, 0, 0] #initial concentrations (cells/nL , cells/nL , nM , nM)
tspan = [0, 400] # time span (h)
teval = np.arange(0, tspan[1]+1, 1) 
sol = solve_ivp(lambda t,C: PredPray(t,C,kc1,kc2,cmax,beta,dc1,dc2,K1,K2,kA1,kA2,d_Ae1,d_Ae2,D), tspan, C0, method = 'RK45', t_eval=teval)
axins = il.inset_axes(axs, "30%", "30%", loc='lower left', borderpad=0,
    bbox_to_anchor=(0.2,0.2,0.7,0.4),bbox_transform=axs.transAxes)
axins.plot(sol.t, sol.y[0], label='Predator')
axins.plot(sol.t, sol.y[1], label='Prey')
axins.set_xlabel('Time')
axins.set_ylabel('Cells')
## mono prey *******************************************************************
dc1 = 0.5 + 1*(10**2)/(25+10**2) # death rate for 1 (h^-1)
kA2 = 0.02 + 0.03*(10**2)/(25+10**2) # AHL 2 synthesis rate (nM.mL/h)
D=0.175
# ODEs for cells and AHL    
C0 = [20, 20, 0, 0] #initial concentrations (cells/nL , cells/nL , nM , nM)
tspan = [0, 400] # time span (h)
teval = np.arange(0, tspan[1]+1, 1) 
sol = solve_ivp(lambda t,C: PredPray(t,C,kc1,kc2,cmax,beta,dc1,dc2,K1,K2,kA1,kA2,d_Ae1,d_Ae2,D), tspan, C0, method = 'RK45', t_eval=teval)
axins = il.inset_axes(axs, "30%", "30%", loc='lower left', borderpad=0,
    bbox_to_anchor=(0.73,0.7,0.7,0.4),bbox_transform=axs.transAxes)
axins.plot(sol.t, sol.y[0], label='Predator')
axins.plot(sol.t, sol.y[1], label='Prey')
axins.set_xlabel('Time')
axins.set_ylabel('Cells')
## bistable ********************************************************************
dc1 = 0.5 + 1*(100**2)/(25+100**2) # death rate for 1 (h^-1)
kA2 = 0.02 + 0.03*(100**2)/(25+100**2) # AHL 2 synthesis rate (nM.mL/h)
D=0.1
# ODEs for cells and AHL    
C0 = [20, 20, 0, 0] #initial concentrations (cells/nL , cells/nL , nM , nM)
tspan = [0, 400] # time span (h)
teval = np.arange(0, tspan[1]+1, 1) 
sol = solve_ivp(lambda t,C: PredPray(t,C,kc1,kc2,cmax,beta,dc1,dc2,K1,K2,kA1,kA2,d_Ae1,d_Ae2,D), tspan, C0, method = 'RK45', t_eval=teval)
axins = il.inset_axes(axs, "30%", "30%", loc='lower left', borderpad=0,
    bbox_to_anchor=(0.25,0.7,0.7,0.4),bbox_transform=axs.transAxes)
axins.plot(sol.t, sol.y[0], label='Predator')
axins.plot(sol.t, sol.y[1], label='Prey')
axins.set_xlabel('Time')
axins.set_ylabel('Cells')


