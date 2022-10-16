# Libraries *******************************************************************
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
import scipy, scipy.optimize

# Import data *****************************************************************
df = pd.read_csv(r'C:\Users\bruno\OneDrive\Documentos\GitHub\biotech-code-examples\Enzyme activity - surface plot\enz_activity.csv')

mean=[]
sd=[]
for i in range(len(df.Rx1)):
    mean.append(df.at[i,'Blank (no rx)']-(sum(df.iloc[i,3:])/3))
    sd.append(np.std(df.iloc[i,3:]))


# Plot scattered points *******************************************************
plt.style.use(r'C:\Users\bruno\OneDrive\Documentos\GitHub\biotech-code-examples\style_preset\plot_preset.mplstyle')
fig = plt.figure()

ax = plt.axes(projection='3d')

ax.errorbar(df['Temperature'], df['pH'], mean, zerr=sd, fmt='o', ecolor='lightgray', elinewidth=2, capsize=3)

ax.set_xlabel('Temperature (°C)', labelpad=15)
ax.set_ylabel('pH', labelpad=15)
ax.set_zlabel('Enz Activity', labelpad=15)


# Custom color map ************************************************************
def hex_to_rgb(value):
    '''
    Converts hex to rgb colours
    value: string of 6 characters representing a hex colour.
    Returns: list length 3 of RGB values'''
    value = value.strip("#") # removes hash symbol if present
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_dec(value):
    '''
    Converts rgb to decimal colours (i.e. divides each value by 256)
    value: list (length 3) of RGB values
    Returns: list (length 3) of decimal values'''
    return [v/256 for v in value]

def get_continuous_cmap(hex_list, float_list=None):
    ''' creates and returns a color map that can be used in heat map figures.
        If float_list is not provided, colour map graduates linearly between each color in hex_list.
        If float_list is provided, each color in hex_list is mapped to the respective location in float_list. 
        
        Parameters
        ----------
        hex_list: list of hex code strings
        float_list: list of floats between 0 and 1, same length as hex_list. Must start with 0 and end with 1.
        
        Returns
        ----------
        colour map'''
    rgb_list = [rgb_to_dec(hex_to_rgb(i)) for i in hex_list]
    if float_list:
        pass
    else:
        float_list = list(np.linspace(0,1,len(rgb_list)))
        
    cdict = dict()
    for num, col in enumerate(['red', 'green', 'blue']):
        col_list = [[float_list[i], rgb_list[i][num], rgb_list[i][num]] for i in range(len(float_list))]
        cdict[col] = col_list
    cmp = mcolors.LinearSegmentedColormap('my_cmp', segmentdata=cdict, N=256)
    return cmp


hex_list = ['364B9A', '4A7BB7', '6EA6CD', '98CAE1', 'C2E4EF', 'EAECCC', 'FEDA8B', 'FDB366', 'F67E4B', 'DD3D2D', 'A50026']


# Quadratic curve fit *********************************************************

Temp = df['Temperature'].values.tolist()
pH = df['pH'].values.tolist()
data = [Temp, pH, mean]

def func(data, a, b, c, d, e, f):
    Temp = data[0]
    pH = data[1]
    return a + b*Temp + c*pH + d*Temp*pH + e*Temp**2 + f*pH**2

initialParameters = [1, 1, 1, 1, 1, 1]

# here a non-linear surface fit is made with scipy's curve_fit()
fit_param, pcov = scipy.optimize.curve_fit(func, [Temp, pH], mean, p0 = initialParameters)

print('Fitted prameters:', fit_param)

modelPredictions = []
absError = []
for i in range(len(Temp)):
    fit=fit_param[0] + fit_param[1]*Temp[i] + fit_param[2]*pH[i] + fit_param[3]*Temp[i]*pH[i] + fit_param[4]*Temp[i]**2 + fit_param[5]*pH[i]**2
    modelPredictions.append(fit)
    err = fit - mean[i]
    absError.append(err)

SE = np.square(absError) # squared errors
MSE = np.mean(SE) # mean squared errors
RMSE = np.sqrt(MSE) # Root Mean Squared Error, RMSE
Rsquared = 1.0 - (np.var(absError) / np.var(mean))

print('RMSE:', RMSE)
print('R-squared:', Rsquared)


# Plot fitted curve ***********************************************************

xModel = np.linspace(min(Temp), max(Temp), 20)
yModel = np.linspace(min(pH), max(pH), 20)
X, Y = np.meshgrid(xModel, yModel)
Z = func(np.array([X, Y]), *fit_param)

cset = ax.contourf(X, Y, Z, zdir='z', offset=-1, cmap=get_continuous_cmap(hex_list), levels=20)
cbr = ax.plot_surface(X,Y,Z, cmap=get_continuous_cmap(hex_list),alpha=0.5)

#plt.colorbar(cbr) # add colorbar
ax.view_init(25,150) # viewing angle

#project data shadows
z=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
ax.scatter3D(df['Temperature'], df['pH'], z, color='gray', alpha=0.1)

# Calculate max activity
max_x = scipy.optimize.fmin(lambda x: -func(x,*fit_param), [1,1])
print('Predicted max activity: {:.2f}°C, pH {:.2f}'.format(max_x[0],max_x[1]))
