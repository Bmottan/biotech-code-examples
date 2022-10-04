# Libraries
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

# Load image with numbers in a table
bac = mpimg.imread(r"C:\Users\bruno\OneDrive\Documentos\GitHub\biotech-code-examples\Image SVD\bacteria.jpg") 

bac_g = rgb2gray(bac); # Convert RGB to grayscale


# Define plot space

fig, axarr = plt.subplots(2,3, figsize=(25, 10))
fig.suptitle("Image SVD transformation", fontsize =20, fontweight='bold')

axarr[0,0].imshow(bac_g)
plt.set_cmap('gray')
fig.text(0.225,0.9,'Original',fontsize =15)
axarr[0,0].axis('off')

U, S, VT = np.linalg.svd(bac_g,full_matrices=False)
S = np.diag(S)

r=5
X5 = U[:,:r] @ S[0:r,:r] @ VT[:r,:]
axarr[0,1].imshow(X5)
plt.set_cmap('gray')
fig.text(0.5,0.9,'r=5',fontsize =15)
axarr[0,1].axis('off')
r=10
X10 = U[:,:r] @ S[0:r,:r] @ VT[:r,:]
axarr[0,2].imshow(X10)
plt.set_cmap('gray')
fig.text(0.775,0.9,'r=10',fontsize =15)
axarr[0,2].axis('off')
r=50
X50 = U[:,:r] @ S[0:r,:r] @ VT[:r,:]
axarr[1,0].imshow(X50)
plt.set_cmap('gray')
fig.text(0.225,0.475,'r=50',fontsize =15)
axarr[1,0].axis('off')
r=1365
X1365 =U[:,:r] @ S[0:r,:r] @ VT[:r,:]
axarr[1,1].imshow(X1365)
plt.set_cmap('gray')
fig.text(0.5,0.475,'r=1365',fontsize =15)
axarr[1,1].axis('off')


axarr[1,2].plot(100*np.cumsum(np.diag(S))/np.sum(np.diag(S)))
plt.title('Singular Values: Cumulative Sum', fontsize=15)
axarr[1,2].set_xlabel('Number of singular vectors (r)', loc='center', fontsize=12)
axarr[1,2].set_ylabel('Explained variance (%)', loc='center', fontsize=12)
plt.grid(which='major', axis='both', alpha=0.1)
plt.show()
