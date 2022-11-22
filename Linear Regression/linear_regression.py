# Libraries *******************************************************************
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.metrics import r2_score

# Import data *****************************************************************
df = pd.read_csv(r'C:\Users\bruno\OneDrive\Documentos\GitHub\biotech-code-examples\Linear Regression\std_curve.csv')

df['mean'] = np.mean(df.iloc[:,1:4], axis=1)
df['mean-blk'] = df['mean']-df['mean'][0]
df['std'] = np.std(df.iloc[:,1:4], axis=1)

# Linear model ****************************************************************
regr = linear_model.LinearRegression()
train_x = np.asanyarray(df[['Protein']])
train_y = np.asanyarray(df[['mean-blk']])
regr.fit(train_x[1:-2], train_y[1:-2]) # fit removing last 2 points (saturation) and blank
R2 = r2_score(train_y[1:-2], regr.coef_[0][0]*train_x[1:-2] + regr.intercept_[0])

# Coefficients ****************************************************************
print ('Coefficients: ', regr.coef_)
print ('Intercept: ',regr.intercept_)
print("R2-score: %.4f" % R2 )

# Plot*************************************************************************
plt.style.use(r'C:\Users\bruno\OneDrive\Documentos\GitHub\biotech-code-examples\style_preset\plot_preset.mplstyle')
plt.figure()
plt.suptitle("Protein Standard Curve",fontsize=20,fontweight='bold')

plt.errorbar(df['Protein'], df['mean-blk'], yerr=df['std'], fmt="o", ecolor='black', capsize=8, color='blue')
plt.errorbar(df['Protein'][-2:], df['mean-blk'][-2:], yerr=df['std'][-2:], fmt="o", color='gray') #removed points
plt.plot(train_x[1:-2], regr.coef_[0][0]*train_x[1:-2] + regr.intercept_[0], '-r')
plt.xlabel("$\mu g$ protein")
plt.ylabel("Abs (595nm)")
plt.text(x=9, y=0.05, s="ABS = {}*PROT + {} \n$R^2 =$ {:.4f}".format(regr.coef_,regr.intercept_,R2), ha='left', fontsize=14)



