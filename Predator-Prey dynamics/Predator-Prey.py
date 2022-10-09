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
fig2, axs = plt.subplots(1,1, figsize=(20,20))

axs.scatter(*zip(*monostable_predator), marker="s", s=100, label='Predator domination')
axs.scatter(*zip(*monostable_prey), marker="s", s=100, label='Prey domination')
axs.scatter(*zip(*bistable), marker="s", s=100, label='Oscillatory behavior')
axs.legend(loc='upper center', bbox_to_anchor=(0.2, 0.9), 
           frameon=True, ncol=1, fontsize=18)
axs.set_xlabel('kc1 ($h^{-1}$)', loc='center', fontsize=18, labelpad=15)
axs.set_ylabel('dc1 ($h^{-1}$)', loc='center', fontsize=18, labelpad=15)
axs.set_title('Bifurcation plot for predator \n growth vs death rates', fontsize=20, fontweight='bold')

#%%

# Bifurcation Dilution x IPTG

# Parameters %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

kc1 = 0.8; #specific growth rate for 1 (h^-1)
kc2 = 0.4; #specific growth rate for 2(h^-1)
cmax = 100; #carrying capacity for cell growth (10^3 cells/nL)
beta = 2; #Cooperativity of AHL effect
kA1 = 0.1; # AHL 1 synthesis rate (nM.mL/h)
d_Ae1 = 0.017; # AHL 1 extracellular decay rate constant (h^-1)
d_Ae2 = 0.11; # AHL 2 extracellular decay rate constant (h^-1)
Dil = linspace(0,0.2,100); # dilution rate (h^-1)
K1 = 10; #Concentration of AHL necessary to half max activity of PluxI promoter (nM)
K2 = K1; #Concentration of AHL necessary to half max activity of PluxI promoter (nM)
IPTG = logspace(0,3,100); #IPTG concentration (uM)
dc2 = 0.3; # death rate for 2 (h^-1)



# Solve ODEs %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
bifurc=zeros(100);
for i=1:100 #column (D)
    for j=1:100 #row (IPTG)
        intersec=0;
        dc1 = 0.5+1*(IPTG(j)^2)/(25+IPTG(j)^2); # death rate for 1 (h^-1)
        kA2 = 0.02+0.03*(IPTG(j)^2)/(25+IPTG(j)^2); # AHL 2 synthesis rate (nM.mL/h)
        D=Dil(i);
    # ODEs for cells and AHL %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    tspan = [0:1:400]; #time span (h)
    C_0 = [20,20,0,0] ; #initial concentrations (cells/nL , cells/nL , nM , nM) 
    [t,C] = ode45(@(t,C) PredPray( t,C,kc1,kc2,cmax,beta,dc1,dc2,K1,K2,kA1,kA2,d_Ae1,d_Ae2,D ),tspan,C_0);
    for k=1:size(C,1)
        diff(k)=sign(C(k,1)-C(k,2));
    end
    for o=100:size(diff,2)
            if diff(o)==diff(o-1)
                intersec=intersec;
            else
                intersec=intersec+1;
            end
    end
     if intersec>0
           bifurc(j,i)=1;
        else
           bifurc(j,i)=0;
        end
    end
end

#plot
figure(3)
W=mat2gray(bifurc);
imshow(W)
title('Bifurcation analysis','fontsize',18)


# Introduction of noise


# Replicate Figure 2 Oscillations
# Parameters %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

kc1 = 0.8; #specific growth rate for 1 (h^-1)
kc2 = 0.4; #specific growth rate for 2(h^-1)
cmax = 100; #carrying capacity for cell growth (10^3 cells/nL)
beta = 2; #Cooperativity of AHL effect
kA1 = 0.1; # AHL 1 synthesis rate (nM.mL/h)
d_Ae1 = 0.017; # AHL 1 extracellular decay rate constant (h^-1)
d_Ae2 = 0.11; # AHL 2 extracellular decay rate constant (h^-1)
D = 0.1125; # dilution rate (h^-1)
K1 = 10; #Concentration of AHL necessary to half max activity of PluxI promoter (nM)
K2 = K1; #Concentration of AHL necessary to half max activity of PluxI promoter (nM)
IPTG = [0,5,1000]; #IPTG concentration (�M)
dc2 = 0.3; # death rate for 2 (h^-1)
n=[0 0.005 0.01 0.025 0.05]; # noise level

# Plot ODEs %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
figure(4)
p=1;
for j=1:5
    noise=n(j);
for i=1:3
    dc1 = 0.5+1*(IPTG(i)^2)/(25+IPTG(i)^2); # death rate for 1 (h^-1)
    kA2 = 0.02+0.03*(IPTG(i)^2)/(25+IPTG(i)^2); # AHL 2 synthesis rate (nM.mL/h)
    # ODEs for cells and AHL %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    tspan = [0:1:400]; #time span (h)
    C_0 = [20,20,0,0] ; #initial concentrations (cells/nL , cells/nL , nM , nM) 
    [t,C] = ode45(@(t,C) PredPray2( t,C,kc1,kc2,cmax,beta,dc1,dc2,K1,K2,kA1,kA2,d_Ae1,d_Ae2,D,noise ),tspan,C_0);
    # plot
    subplot(5,3,p)
    plot(t,C(:,1),'r',t,C(:,2),'b')
    xlabel('t (h)','fontsize',14)
    ylabel('x10^3 cells/nL','fontsize',14)
    title(['IPTG=' num2str(IPTG(i)),'�M'],'fontsize',14)
    legend('Predator','Prey')
    set(gca,'fontsize',14)
    
    p=p+1;

end

end


