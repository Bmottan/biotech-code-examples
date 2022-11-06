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
import random

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
# 'Python pairwise comparison letter generator'
# Github: PhilPlantMan
# https://github.com/PhilPlantMan/Python-pairwise-comparison-letter-generator/blob/master/pairwisecomp_letters.py
#******************************************************************************

def multi_comparisons_letter_df_generator(comparisons_df, letter_ordering_series = None, 
                                          primary_optimisation_parameter = "Number of different letters", 
                                          monte_carlo_cycles = 5, letter_separator = '', ): 
    """
    Function takes a df listing pairwise comparisons with a cols labelled 'group1' and 'group2' for the two groups being compared 
    and another column labelled 'reject' with boolean values corresponding to whether the null hypothesis should be rejected 
    i.e. True: Both treatments are significantly different
    
    letter_ordering_series (default = None): In theory, which letters are assigned to each non-significance grouping is
    arbitrary and therefor the order can be changed. Offering letter_ordering_series a series with the same index as the output
    will make sure that the order that letters are assigned will follow letter_ordering_series from max to min. For boxplots,
    letter_ordering_series with median values is a good choice.
    
    monte_carlo_cycles (default = 5): Function will always return correct letter representation however it may be suboptimal. 
    Within each monte carlo cycle, a random letter is deleted until the representation breaks. The result with the optimum
    number layout of letters after n monte_carlo_cycles is returned. 
    
    The optimum letter layout is set by primary_optimisation_parameter (default = "Number of different letters"):
        'Number of different letter' optimises for fewest different letters
        "Min letters per row" optimises for the fewest letters assigned per treatment
        "Letter total" optimises for the fewest total letters of the treatments combined
        
    letter_separator (default = ''): Separator for each letter in string assigned to each treatment
    
    
    Letter representation is determined by the method described by Piepho 2004: An Algorithm for a Letter-Based Representation
    of All-Pairwise Comparisons
    """
    #'Insert' stage
    #make df with all unique groups as index
    letters_df = comparisons_df['group1'].append(comparisons_df['group2']).drop_duplicates().to_frame().set_index(0)
    
    letters_df[letters_df.shape[1]] = 1
    for pos_result in comparisons_df.loc[comparisons_df['reject']==True].index:
        group1 = comparisons_df.loc[pos_result, 'group1']
        group2 = comparisons_df.loc[pos_result, 'group2']
        for letter_col in letters_df:
            group1_val = letters_df.loc[group1,letter_col]
            group2_val = letters_df.loc[group2,letter_col]
            if group1_val == 1 and group2_val == 1:
                #duplicate column
                new_col = letters_df.shape[1]
                letters_df[new_col] = letters_df[letter_col]
                #del val at group1 first col and at group2 new col
                letters_df.loc[group1,letter_col] = 0
                letters_df.loc[group2,new_col] = 0
    #'Absorb' stage          
    for col in letters_df:
       other_cols_list = list(letters_df)
       other_cols_list.remove(col)
       col_total = letters_df[col].sum()
       for other_col in other_cols_list:
           matched_total = 0
           for row in letters_df.index:
               if letters_df.loc[row, col] == 1 and letters_df.loc[row, other_col]: matched_total +=1
           if col_total == matched_total:
               letters_df.drop(col, axis = 1, inplace = True)  
               break
        
    def check_letters_against_tests(test_df, letters_df):
        if letters_df.sum(axis = 1).min() == 0: return False
        for result_row in test_df.index:
            group1 = test_df.loc[result_row, 'group1']
            group2 = test_df.loc[result_row, 'group2']
            reject = bool(test_df.loc[result_row, 'reject'])
            count_of_true_trues = 0
            count_of_true_falses = 0
            for letter_col in letters_df:
                group1_val = letters_df.loc[group1,letter_col]
                group2_val = letters_df.loc[group2,letter_col]
                if reject:
                    if group1_val != group2_val: count_of_true_trues += 1
                    if group1_val == 1 and group2_val == 1: 
                        return False
                if reject == False:
                    if group1_val == 1 and group2_val == 1: count_of_true_falses += 1
            if reject and count_of_true_trues == 0: 
                return False
            if reject == False and count_of_true_falses == 0: 
                return False
        return True

    #'Sweep stage' with monte carlo optimisation
    for i in range(monte_carlo_cycles):
        num_of_letters = letters_df.sum().sum()
        num_list = list(np.arange(start = 1, stop = 1+ num_of_letters))
        letters_df_monte_order = letters_df.copy()
        for row in letters_df_monte_order.index:
            for col in letters_df_monte_order:
                if letters_df_monte_order.loc[row,col] == 0: continue
                random_num = random.sample(num_list, 1)[0]
                letters_df_monte_order.loc[row,col] = random_num
                num_list.remove(random_num)
        
        current_letters_df = letters_df.copy()
        for pos in range(num_of_letters + 1):     
            mask = letters_df_monte_order.isin([pos])
            zero_df = letters_df.copy().loc[:] = 0
            letters_df_copy = current_letters_df.copy()
            letters_df_copy.mask(mask, other = zero_df, inplace = True)
            if check_letters_against_tests(comparisons_df,letters_df_copy):
                current_letters_df = letters_df_copy
        
        for col in letters_df:
            if current_letters_df[col].sum() == 0: current_letters_df.drop(col, axis = 1, inplace = True)
            
        # determine fitness parameters for optimisation
        current_fitness_parameter_vals = {"Min letters per row":current_letters_df.sum(axis = 1).max(),
                                          "Number of different letters": current_letters_df.shape[1],
                                          "Letter total": current_letters_df.sum().sum()}
        if i == 0: 
            best_fitness_parameter_vals = current_fitness_parameter_vals
            best_letters_df = current_letters_df
            continue
        
        if current_fitness_parameter_vals[primary_optimisation_parameter] > best_fitness_parameter_vals[primary_optimisation_parameter]:
            continue
        if current_fitness_parameter_vals[primary_optimisation_parameter] < best_fitness_parameter_vals[primary_optimisation_parameter]:
            best_letters_df = current_letters_df.copy()
            best_fitness_parameter_vals = current_fitness_parameter_vals
            
        if sum(current_fitness_parameter_vals.values()) < sum(best_fitness_parameter_vals.values()):
            best_letters_df = current_letters_df.copy()
            best_fitness_parameter_vals = current_fitness_parameter_vals
    
    #order cols
    if isinstance(letter_ordering_series, pd.Series):
        scoring_df = pd.DataFrame(index = best_letters_df.index)
        for row in best_letters_df.index:
            for col in best_letters_df:
                scoring_df.loc[row, col] = best_letters_df.loc[row, col] * letter_ordering_series[row]
        scoring_df = scoring_df.replace(0, np.NaN)
        scoring_means = scoring_df.mean(axis = 0).sort_values(ascending = False)
        best_letters_df = best_letters_df[scoring_means.index]
    # letter the cols     
    for col_name, col_num in zip(best_letters_df, range(len(best_letters_df.columns))):
        letter = string.ascii_lowercase[col_num]
        best_letters_df.loc[best_letters_df[col_name] == 1, col_name] = letter
    # make df with strings ready for presentation
    best_string_df = pd.DataFrame(index = best_letters_df.index)
    best_string_df.loc[:,'string'] = ""
    for row in best_letters_df.index:
        for col in best_letters_df:
            if best_letters_df.loc[row, col] != 0:
                letter_string = best_string_df.loc[row, 'string']
                letter = best_letters_df.loc[row, col]
                if letter_string == "": best_string_df.loc[row, 'string'] = letter
                else: best_string_df.loc[row, 'string'] = letter_separator.join((letter_string, letter))
                
    return best_string_df
#******************************************************************************

def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
         raise ValueError

#******************************************************************************

# Compact letter display for Protein ******************************************

result = m_comp._results_table.as_csv() #get results separated by comma
result_csv = result.replace(m_comp._results_table.title,'') # remove title
data = StringIO(result_csv)
dftable = pd.read_csv(data) # results as pandas dataframe
         
for i in range(len(dftable.reject)):
    dftable.at[i,'reject'] = str_to_bool(dftable.at[i,'reject'].strip()) # remove whitespace

cld_prot = multi_comparisons_letter_df_generator(dftable)

cld_prot_ix = []
for i in range(len(cld_prot)):
    cld_prot.string[i] = ','.join(cld_prot.string[i]) # add commas
    cld_prot_ix.append(cld_prot.index[i].strip()) # remove whitespace



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

for i in range(len(dftable.reject)):
    dftable.at[i,'reject'] = str_to_bool(dftable.at[i,'reject'].strip()) # remove whitespace

cld_act = multi_comparisons_letter_df_generator(dftable)

cld_act_ix = []
for i in range(len(cld_act)):
    cld_act.string[i] = ','.join(cld_act.string[i]) # add commas
    cld_act_ix.append(cld_act.index[i].strip()) # remove whitespace

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


# Plot ************************************************************************
plt.style.use(r'C:\Users\bruno\OneDrive\Documentos\GitHub\biotech-code-examples\style_preset\plot_preset.mplstyle')
fig, axs = plt.subplots(1,2, figsize=(20,10))
fig.suptitle("Enzyme Expression",fontsize =20,fontweight='bold')

axs[0].bar(amostra,prot_mean, yerr=prot_sd, alpha=0.8, ecolor='black', capsize=10)
axs[0].set_xlabel('Sample')
axs[0].set_ylabel('Protein (mg/L)')
axs[0].set_title('Total Protein')
for s in range(len(amostra)):
    idx = cld_act_ix.index(amostra[s])
    code = cld_prot.string[idx]
    axs[0].text(x=s,y=prot_mean[s]+prot_sd[s]+2,s=code,ha='center',size='10')


axs[1].bar(amostra,act_mean, yerr=act_sd, color='#EE6677', alpha=0.8, ecolor='black', capsize=10)
axs[1].set_xlabel('Sample')
axs[1].set_ylabel('Enzymatic Activity (U/mL)')
axs[1].set_title('Enzyme activity')
for s in range(len(amostra)):
    idx = cld_act_ix.index(amostra[s])
    code = cld_act.string[idx]
    axs[1].text(x=s,y=act_mean[s]+act_sd[s]+0.015,s=code,ha='center',size='10')
