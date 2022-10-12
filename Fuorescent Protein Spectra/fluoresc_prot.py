# One FP, Ex and Em spectra

# Libraries
import matplotlib.pyplot as plt
import pandas as pd

# Convert wavelength (nm) to RGB:
def wavelength_to_rgb(wavelength, gamma=0.8):
    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 750:
        A = 1. # visible range, alpha = 1
    else:
        A = 0.5  # outside visible range, alpha = 0.5
    if wavelength < 380:
        wavelength = 380.
    if wavelength > 750:
        wavelength = 750.
    if 380 <= wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif 440 <= wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif 490 <= wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif 510 <= wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif 580 <= wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif 645 <= wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    return (R, G, B, A)


# Spectrum data

df = pd.read_csv(r'C:\Users\bruno\OneDrive\Documentos\GitHub\biotech-code-examples\Fuorescent Protein Spectra\sfGFP.csv')

wave_ex = df.loc[df.ex.idxmax(), 'wavelength']
color_ex = wavelength_to_rgb(wave_ex)
wave_em = df.loc[df.em.idxmax(), 'wavelength']
color_em = wavelength_to_rgb(wave_em)

# Plot
plt.style.use(r'C:\Users\bruno\OneDrive\Documentos\GitHub\biotech-code-examples\style_preset\plot_preset.mplstyle')
plt.figure()

plt.plot(df.wavelength,df.ex, color=color_ex, label='Ex (max={})'.format(wave_ex))
x = range(0,len(df.wavelength))
y = df.ex[x]
plt.fill_between(df.wavelength, y, color=color_ex, alpha=0.2)
plt.plot(df.wavelength,df.em, color=color_em, label='Em (max={})'.format(wave_em))
x = range(0,len(df.wavelength))
y = df.em[x]
plt.fill_between(df.wavelength, y, color=color_em, alpha=0.2)

plt.legend(loc='upper right',frameon=True)
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity')


#%%

# All FP, Em spectra

# Libraries
import matplotlib.pyplot as plt
import pandas as pd

# Convert wavelength (nm) to RGB:
def wavelength_to_rgb(wavelength, gamma=0.8):
    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 750:
        A = 1. # visible range, alpha = 1
    else:
        A = 0.5  # outside visible range, alpha = 0.5
    if wavelength < 380:
        wavelength = 380.
    if wavelength > 750:
        wavelength = 750.
    if 380 <= wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif 440 <= wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif 490 <= wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif 510 <= wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif 580 <= wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif 645 <= wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    return (R, G, B, A)




FP = ['mTagBFP2','Cerulean','EGFP','mCitrine','mOrange','tdTomato','mCherry']

plt.style.use(r'C:\Users\bruno\OneDrive\Documentos\GitHub\biotech-code-examples\style_preset\plot_preset.mplstyle')
plt.figure()

for i in range(len(FP)):
    folder = r'C:\Users\bruno\OneDrive\Documentos\GitHub\biotech-code-examples\Fuorescent Protein Spectra\\'
    df = pd.read_csv(folder + FP[i] +'.csv')
    #wave_ex = df.loc[df.ex.idxmax(), 'wavelength']
    #color_ex = wavelength_to_rgb(wave_ex)
    wave_em = df.loc[df.em.idxmax(), 'wavelength']
    color_em = wavelength_to_rgb(wave_em)

    # Plot
    #plt.plot(df.wavelength,df.ex, color=color_ex, label='Ex (max={})'.format(wave_ex))
    #x = range(0,len(df.wavelength))
    #y = df.ex[x]
    #plt.fill_between(df.wavelength, y, color=color_ex, alpha=0.2)
    plt.plot(df.wavelength,df.em, color=color_em, label='{} (max={})'.format(FP[i],wave_em))
    x = range(0,len(df.wavelength))
    y = df.em[x]
    plt.fill_between(df.wavelength, y, color=color_em, alpha=0.2)

    plt.legend(loc='upper right',frameon=True)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Intensity')


