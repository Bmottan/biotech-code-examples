# Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
import math
import pygad

# Import data
df = pd.read_csv(r'C:\Users\bruno\OneDrive\Documentos\GitHub\biotech-code-examples\Genetic algorithm\batchdata.csv')
solutions = []

#Plot all data ***************************************************************
# Define plot space
fig1, axs = plt.subplots(1,2,figsize=(20,10))
fig1.suptitle("Batches data", fontsize =20, fontweight='bold')

# Data: Cells
axs[0].scatter(df.iloc[:,0],df.iloc[:,1],label='Run 1')
axs[0].scatter(df.iloc[:,3],df.iloc[:,4],label='Run 2')
axs[0].scatter(df.iloc[:,6],df.iloc[:,7],label='Run 3')
axs[0].scatter(df.iloc[:,9],df.iloc[:,10],label='Run 4')
axs[0].scatter(df.iloc[:,12],df.iloc[:,13],label='Run 5')
axs[0].set_xlabel('Time')
axs[0].set_ylabel('Cells')
axs[0].set_title('Cells', fontsize=15, fontweight='bold')
axs[0].legend(loc='upper center', bbox_to_anchor=(0.1, 1), 
           frameon=False, ncol=1, fontsize=15)

# Data: Substrate
axs[1].scatter(df.iloc[:,0],df.iloc[:,2],label='Run 1')
axs[1].scatter(df.iloc[:,3],df.iloc[:,5],label='Run 2')
axs[1].scatter(df.iloc[:,6],df.iloc[:,8],label='Run 3')
axs[1].scatter(df.iloc[:,9],df.iloc[:,11],label='Run 4')
axs[1].scatter(df.iloc[:,12],df.iloc[:,14],label='Run 5')
axs[1].set_xlabel('Time')
axs[1].set_ylabel('Substrate')
axs[1].set_title('Substrate', fontsize=15, fontweight='bold')
axs[1].legend(loc='upper center', bbox_to_anchor=(0.9, 1), 
           frameon=False, ncol=1, fontsize=15)

#*****************************************************************************



# System Model Function
def dy(t,y):
    #**********************************************
    # Variables:
    #   y[0] : X
    #   y[1] : S
    #   param = [mu_max,Ks,Ki,mu_s]
    #**********************************************
    
    param = solutions
    mu_max = param[0]
    Ks = param[1]
    Ki = param[2]
    Yxs = param[3]
    
    # Cells (X)
    #mu_max = 0.3     # (h^-1) 
    #Ks = 0.01           # (g/L)
    #mu = mu_max*S/(Ks+S+(S*S/Ki)) # (h^-1) specific growth rate - Haldane-Andrews

    # Substrate (S)

    #Yxs = 0.2        # (g_cell/g_sub) cell yield
    #mu_s = mu/Yxs    # (g_sub/g_cell.h) specific consumption rate

    #**********************************************    
    dy = [0,0]
    
    rx = mu_max*y[1]*y[0]/(Ks+y[1]+(y[1]*y[1]/Ki))
    rs = rx/Yxs
    
    dy[0] = rx
    dy[1] = -rs
    
    return dy
#*****************************************************************************

# Fitness eval
def fitness_func(solution, solution_idx):
    global df
    global solutions
    val = 0
    solutions = solution
    
    for i in range(1,6): #for all 5 batches
        ic=3*(i-1)
        Td = df.iloc[:,ic] #time data
        Yd = df.iloc[:,ic+1:ic+3] #X and S data
        Yc0 = [Yd.iloc[0,0],Yd.iloc[0,1]] #initial point t=0
        tspan = [0, Td.iloc[-1]]
        teval = np.arange(0, tspan[1]+0.5, 0.5)
        sol = solve_ivp(dy, tspan, Yc0, method = 'LSODA', t_eval=teval);
    
        X = sol.y[0]
        S = sol.y[1]

        # data-prediction difference
        for i in range(len(Yd)):
            for j in range(0,2):
                if j==0:
                    dz=(Yd.iloc[i,j]-X[i])**2;
                    val=val+dz;
                elif j==1:
                    dz=(Yd.iloc[i,j]-S[i])**2;
                    val=val+dz;   
        fitness = 1 / (math.sqrt(val))
    return fitness

#*****************************************************************************

# Genetic algorithm
ga_instance = pygad.GA(num_generations=500,
                       num_parents_mating=10, 
                       fitness_func=fitness_func,
                       sol_per_pop=20, 
                       num_genes=4,
                       suppress_warnings=True,
                       gene_space = [{'low': 0.1, 'high': 0.5},
                                     {'low': 0.001, 'high': 0.05},
                                     {'low': 50, 'high': 150},
                                     {'low': 0.15, 'high': 0.35}])

ga_instance.run()
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))

if ga_instance.best_solution_generation != -1:
    print('Best fitness reached at generation {}'.format(ga_instance.best_solution_generation))

#*****************************************************************************

# Plot Best model

# Define plot space
fig2, axs = plt.subplots(5,2,figsize=(20,50))

b=0
for r in range(0,5):
    #Predicted
    solutions = solution
    Td = df.iloc[:,b] #time data
    Yd = df.iloc[:,b+1:b+3] #X and S data run 1
    Yc0 = [Yd.iloc[0,0],Yd.iloc[0,1]] #initial point t=0
    tspan = [0, Td.iloc[-1]]
    teval = np.arange(0, tspan[1]+0.5, 0.5)
    sol = solve_ivp(dy, tspan, Yc0, method = 'LSODA', t_eval=teval);
    
    # Data: Cells
    axs[r,0].scatter(df.iloc[:,b],df.iloc[:,b+1],label='Run {}'.format(r+1))
    axs[r,0].set_xlabel('Time')
    axs[r,0].set_ylabel('Cells')   
    axs[r,0].plot(sol.t, sol.y[0], color = 'magenta',
                  linestyle='-', label='Predicted')
    axs[r,0].legend(loc='upper center', bbox_to_anchor=(0.15, 1), 
                    frameon=False, ncol=1, fontsize=15)

    # Data: Substrate
    axs[r,1].scatter(df.iloc[:,b],df.iloc[:,b+2],label='Run {}'.format(r+1))
    axs[r,1].set_xlabel('Time')
    axs[r,1].set_ylabel('Substrate')
    axs[r,1].plot(sol.t, sol.y[1], color = 'magenta',
                  linestyle='-', label='Predicted')
    axs[r,1].legend(loc='upper center', bbox_to_anchor=(0.85, 1), 
                    frameon=False, ncol=1, fontsize=15)

    b=b+3
    
# Data: GA
fig3 = ga_instance.plot_result()
