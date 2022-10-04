# Libraries
import pandas as pd
from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv(r'C:\Users\bruno\OneDrive\Documentos\GitHub\biotech-code-examples\PCA\wine.csv')
df2 = df.iloc[:,1:] #remove first column

# Preprocessing Data: Scaling
#subtract mean of each column and divide by its standard deviation
dfscale = preprocessing.StandardScaler().fit_transform(df2)

#*******************************************************
#Principal Component Analysis
#*******************************************************

pca = PCA(n_components=10)
projected = pca.fit_transform(dfscale)

#Scores plot - PC1xPC2

fig, axs = plt.subplots(2,2, figsize=(10, 10))
fig.suptitle("PCA of wine data", fontsize =20, fontweight='bold')


axs[0,0].set_title('Scores plot PC1xPC2', fontsize=15, fontweight='bold')
axs[0,0].scatter(projected[:58, 0], projected[:58, 1]) #wine type 1
axs[0,0].scatter(projected[59:129, 0], projected[59:129, 1]) #wine type 2
axs[0,0].scatter(projected[130:177, 0], projected[130:177, 1]) #wine type 3
axs[0,0].set_xlabel('Component 1 ({:.2f}%)'.format(100*pca.explained_variance_ratio_[0]))
axs[0,0].set_ylabel('Component 2 ({:.2f}%)'.format(100*pca.explained_variance_ratio_[1]))


#Loadings plot
loadings = pca.components_
# Get the loadings of x and y axes
xs = loadings[0]
ys = loadings[1]

# Feature names before PCA
feature_names = ['Alcohol','Malic ac','Ash','Ash alk','Magnesium',
                 'Total phenols','Flavanoids','Nonflavanoid phenols',
                 'Proanthocyanins','Color intensity','Hue','OD280/OD315','Proline']

# Plot the loadings on a scatterplot
for i, varnames in enumerate(feature_names):
    axs[0,1].scatter(xs[i], ys[i], s=100)
    axs[0,1].arrow(
        0, 0, # coordinates of arrow base
        xs[i], # length of the arrow along x
        ys[i], # length of the arrow along y
        color='r', 
        head_width=0.01
        )
    axs[0,1].text(xs[i], ys[i], varnames)
axs[0,1].set_xlabel('PC1')
axs[0,1].set_ylabel('PC2')
axs[0,1].set_title('Loadings plot', fontsize=15, fontweight='bold')

#Scree plot - Explained variance
axs[1,0].set_title('Variance', fontsize=15, fontweight='bold')
axs[1,0].bar(range(1,11),pca.explained_variance_) #variance
axs[1,0].set_xlabel('PC')
axs[1,0].set_ylabel('Explained Variance')


axs[1,1].set_title('Cumulative Variance', fontsize=15, fontweight='bold')
axs[1,1].bar(range(1,11),100*np.cumsum(pca.explained_variance_ratio_)) #cumulative variance
axs[1,1].set_xlabel('PC')
axs[1,1].set_ylabel('Cumulative Variance (%)')




