#******************************************************************************
# Test statistical significance between samples 
#******************************************************************************

# Libraries *******************************************************************
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import string
from io import StringIO
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Import data *****************************************************************
df = pd.read_csv(r'C:\Users\bruno\OneDrive\Documentos\GitHub\biotech-code-examples\Statistical difference\Prot_enzact.csv')

amostra = list(df.Amostra.unique()) # list all unique samples

# Group samples ***************************************************************
gr = df.groupby(df.Amostra) # group samples

group_prot = []
for i in amostra:
    g = gr.get_group(i)['Proteina']
    group_prot.append(g)

group_act = []
for i in amostra:
    g = gr.get_group(i)['Atividade']
    group_act.append(g)


# ANOVA oneway - Proteina *****************************************************

fvalue, pvalue = stats.f_oneway(*group_prot)
if pvalue < 0.05:
   text=' -> Significant difference between samples. Perform Tukey HSD.'
else:
    text=' -> No significant difference between samples.'
print(f"Results of ANOVA test for Protein:\n The F-statistic is: {fvalue}\n The p-value is: {pvalue}{text}")


# Multiple pairwise comparison (Tukey HSD) ************************************

m_comp = pairwise_tukeyhsd(endog=df['Proteina'], groups=df['Amostra'], alpha=0.05)
print(m_comp)


#******************************************************************************
# Compact letter display of sig different samples 
# https://github.com/dalensis/compact-letter-display-for-pingouin-python/blob/main/cld.py
#******************************************************************************
def letter_display(df, CI):
    
    alpha = 1-CI/100
    
    '''
    Creates a compact letter display. This creates a dataframe consisting of
    2 columns, a column containing the treatment groups and a column containing
    the letters that have been assigned to the treatment groups. These letters
    are part of what's called the compact letter display. Treatment groups that
    share at least 1 letter are similar to each other, while treatment groups
    that don't share any letters are significantly different from each other.
    Parameters
    ----------
    df : Pandas dataframe
        Pandas dataframe containing raw Tukey test results from statsmodels.
    alpha : float
        The alpha value. The default is 0.05.
    Returns
    -------
    A dataframe representing the compact letter display, created from the Tukey
    test results.
    '''
    df["p-adj "] = df["p-adj "].astype(float)

    # Creating a list of the different treatment groups from Tukey's
    group1 = set(df.group1.tolist())  # Dropping duplicates by creating a set
    group2 = set(df.group2.tolist())  # Dropping duplicates by creating a set
    groupSet = group1 | group2  # Set operation that creates a union of 2 sets
    groups = sorted(list(groupSet))

    # Creating lists of letters that will be assigned to treatment groups
    letters = list(string.ascii_lowercase+string.digits)[:len(groups)]
    cldgroups = letters

    # the following algoritm is a simplification of the classical cld,

    cld = pd.DataFrame(list(zip(groups, letters, cldgroups)))
    cld[3]=""
    
    for row in df.itertuples():
        if df["p-adj "][row[0]] > (alpha):
            cld.iat[groups.index(df["group1"][row[0]]), 2] += cld.iat[groups.index(df["group2"][row[0]]), 1]
            cld.iat[groups.index(df["group2"][row[0]]), 2] += cld.iat[groups.index(df["group1"][row[0]]), 1]
            
        if df["p-adj "][row[0]] < (alpha):
                cld.iat[groups.index(df["group1"][row[0]]), 3] +=  cld.iat[groups.index(df["group2"][row[0]]), 1]
                cld.iat[groups.index(df["group2"][row[0]]), 3] +=  cld.iat[groups.index(df["group1"][row[0]]), 1]

    cld[2] = cld[2].apply(lambda x: "".join(sorted(x)))
    cld[3] = cld[3].apply(lambda x: "".join(sorted(x)))
    cld.rename(columns={0: "groups"}, inplace=True)

    # this part will reassign the final name to the group
    # for sure there are more elegant ways of doing this
    cld["labels"] = ""
    letters = list(string.ascii_lowercase)
    unique = []
    for item in cld[2]:

        for fitem in cld["labels"].unique():
            for c in range(0, len(fitem)):
                if not set(unique).issuperset(set(fitem[c])):
                    unique.append(fitem[c])
        g = len(unique)

        for kitem in cld[1]:
            if kitem in item:
                #Checking if there are forbidden pairing (proposition of solution to the imperfect script)                
                forbidden = set()
                for row in cld.itertuples():
                    if letters[g] in row[5]:
                        forbidden |= set(row[4])
                if kitem in forbidden:
                    g=len(unique)+1
               
                if cld["labels"].loc[cld[1] == kitem].iloc[0] == "":
                   cld["labels"].loc[cld[1] == kitem] += letters[g] 
               
                # Checking if columns 1 & 2 of cld share at least 1 letter
                if len(set(cld["labels"].loc[cld[1] == kitem].iloc[0]).intersection(cld.loc[cld[2] == item, "labels"].iloc[0])) <= 0:
                    if letters[g] not in list(cld["labels"].loc[cld[1] == kitem].iloc[0]):
                        cld["labels"].loc[cld[1] == kitem] += letters[g]
                    if letters[g] not in list(cld["labels"].loc[cld[2] == item].iloc[0]):
                        cld["labels"].loc[cld[2] == item] += letters[g]

    cld = cld.sort_values("labels")
    cld.drop(columns=[1, 2, 3], inplace=True)
    print(cld)
    print('\n')
    print('\n')
    return(cld)
#******************************************************************************

# Compact letter display for Protein ******************************************

result = m_comp._results_table.as_csv() #get results separated by comma
result_csv = result.replace(m_comp._results_table.title,'') # remove title
data = StringIO(result_csv)
dftable = pd.read_csv(data) # results as pandas dataframe

cld_prot = letter_display(dftable,95)



# ANOVA oneway - Atividade ****************************************************

fvalue, pvalue = stats.f_oneway(*group_act)
if pvalue < 0.05:
   text=' -> Significant difference between samples. Perform Tukey HSD.'
else:
    text=' -> No significant difference between samples.'
print(f"Results of ANOVA test for Activity:\n The F-statistic is: {fvalue}\n The p-value is: {pvalue}{text}")


# Multiple pairwise comparison (Tukey HSD) ************************************

m_comp = pairwise_tukeyhsd(endog=df['Atividade'], groups=df['Amostra'], alpha=0.05)
print(m_comp)


# Compact letter display for Activity *****************************************

result = m_comp._results_table.as_csv() #get results separated by comma
result_csv = result.replace(m_comp._results_table.title,'') # remove title
data = StringIO(result_csv)
dftable = pd.read_csv(data) # results as pandas dataframe

cld_act = letter_display(dftable,95)


# Calculate mean and SD *******************************************************
prot_mean = []
prot_sd = []
act_mean = []
act_sd = []
for i in range(len(amostra)):
    prot_mean.append(np.mean(group_prot[i]))
    prot_sd.append(np.std(group_prot[i]))
    act_mean.append(np.mean(group_act[i]))
    act_sd.append(np.std(group_act[i]))

cld_prot.groups = cld_prot.groups.astype(str) # transform to string
cpgroup = []
for s in range(len(amostra)):
    cpgroup.append(cld_prot.groups[s].strip()) # remove whitespace

cld_act.groups = cld_act.groups.astype(str) # transform to string
cagroup = []
for s in range(len(amostra)):
    cagroup.append(cld_act.groups[s].strip()) # remove whitespace


# Plot ************************************************************************
plt.style.use(r'C:\Users\bruno\OneDrive\Documentos\GitHub\biotech-code-examples\style_preset\plot_preset.mplstyle')
fig, axs = plt.subplots(1,2, figsize=(20,10))
fig.suptitle("Enzyme Expression",fontsize =20,fontweight='bold')

axs[0].bar(amostra,prot_mean, yerr=prot_sd, alpha=0.8, ecolor='black', capsize=10)
axs[0].set_xlabel('Sample')
axs[0].set_ylabel('Protein (mg/L)')
axs[0].set_title('Total Protein')
for s in range(len(amostra)):
    idx = cpgroup.index(amostra[s])
    code = cld_prot.labels[idx]
    axs[0].text(x=s,y=prot_mean[s]+prot_sd[s]+2,s=code,ha='center',size='10')


axs[1].bar(amostra,act_mean, yerr=act_sd, color='#EE6677', alpha=0.8, ecolor='black', capsize=10)
axs[1].set_xlabel('Sample')
axs[1].set_ylabel('Enzymatic Activity (U/mL)')
axs[1].set_title('Enzyme activity')
for s in range(len(amostra)):
    idx = cagroup.index(amostra[s])
    code = cld_act.labels[idx]
    axs[1].text(x=s,y=act_mean[s]+act_sd[s]+0.015,s=code,ha='center',size='10')
