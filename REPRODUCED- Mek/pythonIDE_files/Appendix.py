#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 19:16:28 2020

@author: gopaljuneja
"""
import pandas as pd
from termcolor import colored
import numpy as np
import warnings
import statsmodels.formula.api as smf
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

import requests
import os
import sys
sys.path.append('/Users/gopaljuneja/Desktop/Reproduced_MEK')
from regressions import *

dfDandora = pd.io.stata.read_stata(r'/Users/gopaljuneja/Desktop/Microenterprise_Kenya/113714-V1/App2017-0042_data/datasets/BDJ_Dandora_Data.dta')
dfDandora.to_csv('/Users/gopaljuneja/Desktop/Reproduced_MEK/BDJ_Dandora_data.csv')
pd.read_csv(r'/Users/gopaljuneja/Desktop/Reproduced_MEK/BDJ_Dandora_data.csv', index_col = 0)

'''* ------- APPENDIX A: FURTHER BALANCE TESTS'''
for i in range(1,8):
    print("Balance Test: Wave = {}".format(i))
    df_waveFilter = dfDandora.loc[(dfDandora['wave'] == i)]
    groupedTreat = df_waveFilter.groupby('treat')
    '''Wave-by-wave balance tests (Tables 11 -- 17)'''
    for key, value in groupedTreat:
        print('key=' + str(key))
        cols = value.filter(items =['profit_b', 'businessage_b', 'I_emp_b', 'emp_b2', 'credit_b', 'bankaccount_b', 'loan_b', 'formalaccount_b', 'advert_b', 'manu_b', 'retail_b', 'food_b', 'serv_b'])
        print(cols.describe())


#Pearson product-moment correlation coefficients python
dfFilter = dfDandora.loc[(dfDandora['wave'] == 0)]
dfFilter = dfDandora.filter(items =['count','profit_b', 'businessage_b', 'I_emp_b', 'emp_b2', 'credit_b', 'bankaccount_b', 'loan_b', 'formalaccount_b', 'advert_b', 'manu_b', 'retail_b', 'food_b', 'serv_b', 'age_b', 'secondaryedu_b'])
pearsonsCoeff = np.corrcoef([dfFilter['count'], dfFilter.profit_b, dfFilter.businessage_b, dfFilter.I_emp_b, dfFilter.emp_b2, dfFilter.credit_b, dfFilter.bankaccount_b, dfFilter.loan_b, dfFilter.formalaccount_b, dfFilter.advert_b, dfFilter.manu_b, dfFilter.retail_b, dfFilter.food_b, dfFilter.serv_b, dfFilter.age_b, dfFilter.secondaryedu_b], rowvar = True)

'''Correlates with number of surveys taken'''
dataset = pd.DataFrame({'count': pearsonsCoeff[:, 0], 'profit_b': pearsonsCoeff[:, 1],'businessage_b': pearsonsCoeff[:, 2],'I_emp_b': pearsonsCoeff[:, 3],'emp_b2': pearsonsCoeff[:, 4],'credit_b': pearsonsCoeff[:, 5],'bankaccount_b': pearsonsCoeff[:, 6],'loan_b': pearsonsCoeff[:,7],'formalaccount_b': pearsonsCoeff[:, 8],'advert_b': pearsonsCoeff[:, 9],'manu_b': pearsonsCoeff[:, 10],'retail_b': pearsonsCoeff[:, 11],'food_b': pearsonsCoeff[:, 12],'serv_b': pearsonsCoeff[:, 13], 'age_b': pearsonsCoeff[:, 14], 'secondaryedu_b': pearsonsCoeff[:, 15]}, 
                        index=['count','profit_b', 'businessage_b', 'I_emp_b', 'emp_b2', 'credit_b', 'bankaccount_b', 'loan_b', 'formalaccount_b', 'advert_b', 'manu_b', 'retail_b', 'food_b', 'serv_b', 'age_b', 'secondaryedu_b'])

'''*--------------- APPENDIX B: Baseline Learning Methods'''
dfBaseline = pd.io.stata.read_stata(r'/Users/gopaljuneja/Desktop/Microenterprise_Kenya/113714-V1/App2017-0042_data/datasets/BDJ_Baseline_Data.dta')
dfBaseline.to_csv('/Users/gopaljuneja/Desktop/Reproduced_MEK/BDJ_Baseline_data.csv')
pd.read_csv(r'/Users/gopaljuneja/Desktop/Reproduced_MEK/BDJ_Baseline_data.csv', index_col = 0)

dfSortedBaseline = dfBaseline.sort_values(by = 'bl', ascending = True) 


# Loop through rows of dataframe by index i.e. from 0 to number of rows
for i in range(0, dfSortedBaseline.shape[0]-1):
   #get row contents as series and index position of row
   if(dfSortedBaseline['bl'][i] == dfSortedBaseline['bl'][i+1]):
       dfSortedBaseline = dfSortedBaseline.drop(i)
       
dfSortedBaseline.binl = dfSortedBaseline.binl.replace('.', 0)
dfSortedBaseline.binl = pd.to_numeric(dfSortedBaseline.binl)

dfSortedBaseline = dfSortedBaseline[dfSortedBaseline.bl != '.-0']


'''#############################################################################################################################################################################################'''
'''*------------------ APPENDIX C: Details of Mentor Selection'''
df_RDset = pd.io.stata.read_stata(r'/Users/gopaljuneja/Desktop/Microenterprise_Kenya/113714-V1/App2017-0042_data/datasets/RD_Dataset.dta')
df_RDset.to_csv('/Users/gopaljuneja/Desktop/Reproduced_MEK/RD_Dataset.csv')
pd.read_csv(r'/Users/gopaljuneja/Desktop/Reproduced_MEK/RD_Dataset.csv', index_col = 0)

'''Differences between mentees and non-mentees'''
for i in range(0,2):
    df_treatFilter = df_RDset.loc[(df_RDset['treat'] == i)]
    '''Wave-by-wave balance tests (Tables 11 -- 17)'''
    rd_cols = df_treatFilter.filter(items =['profit', 'businessage', 'employees', 'employeesnumber', 'credit', 'bankaccount', 'loan',  'account', 'marketing', 'age', 'secondary_edu'])
    print(rd_cols.describe())

arr =['tprofit', 'tinventory', 'marketing', 'keeps_some_records']
for column in arr:
    print(colored("MSE-Optimal Bandwidth. VAR = {} ... Poly = 0".format(column), "red"))
    r.rdrobust(column, ce_std, c = NULL,  fuzzy = NULL, deriv = NULL, p =0, q = NULL, 
                h = NULL, b = NULL, rho = NULL, covs = NULL,  covs_drop = TRUE, 
                kernel = "tri", weights = NULL, bwselect = "mserd", 
                vce = "nn", cluster = NULL, 
                nnmatch = 3, level = 95, scalepar = 1, scaleregul = 1, 
                sharpbw = FALSE, all = NULL, subset = NULL,
                masspoints = "adjust", bwcheck = NULL)
    


'''#############################################################################################################################################################################################'''
'''*------------------ APPENDIX D: More results'''

'''*------------------ D1. Table 21, column 3'''
dfDandora = pd.io.stata.read_stata(r'/Users/gopaljuneja/Desktop/Microenterprise_Kenya/113714-V1/App2017-0042_data/datasets/BDJ_Dandora_Data.dta')
dfDandora.to_csv('/Users/gopaljuneja/Desktop/Reproduced_MEK/BDJ_Dandora_data.csv')
pd.read_csv(r'/Users/gopaljuneja/Desktop/Reproduced_MEK/BDJ_Dandora_data.csv', index_col = 0)

def filter_by(df, constraints):
    """Filter MultiIndex by sublevels."""
    indexer = [constraints[name] if name in constraints else slice(None)
               for name in df.index.names]
    return df.loc[tuple(indexer)] if len(df.shape) == 1 else df.loc[tuple(indexer),]

pd.Series.filter_by = filter_by
pd.DataFrame.filter_by = filter_by

dfDandora_copy = dfDandora.copy()
dfDandora_copy = dfDandora.set_index(['id', 'wave'])

# Describe 'sec0_b', 'sec1_b', 'sec2_b', 'sec3_b', 'sec4_b'
dffilterW = dfDandora_copy.filter_by({'wave' : [0]})
Fcols = dffilterW.filter(items =['sec0_b', 'sec1_b', 'sec2_b', 'sec3_b', 'sec4_b'])
print(Fcols.describe())

# Describe 'sec0_*'
dffilterW = dfDandora_copy.filter_by({'wave' : [0]})
Fcols1 = dffilterW.filter(items =['sec0_b','sec0_0','sec0_1', 'sec0_2', 'sec0_3','sec0_4', 'sec0_5', 'sec0_6', 'sec0_7', 'sec0_8', 'sec0_9', 'sec0_10'])
print(Fcols1.describe())

# Describe 'sec1_*'
dffilterW = dfDandora_copy.filter_by({'wave' : [0]})
Fcols2 = dffilterW.filter(items =['sec1_b','sec1_1','sec1_2', 'sec1_3', 'sec1_4','sec1_5', 'sec1_6'])
print(Fcols2.describe())

# Describe 'sec2_*'
dffilterW = dfDandora_copy.filter_by({'wave' : [0]})
Fcols3 = dffilterW.filter(items =['sec2_b','sec2_1','sec2_2', 'sec2_3', 'sec2_4','sec2_5', 'sec2_6', 'sec2_7'])
print(Fcols3.describe())

# Describe 'sec3_*'
dffilterW = dfDandora_copy.filter_by({'wave' : [0]})
Fcols4 = dffilterW.filter(items =['sec3_b','sec3_1','sec3_2', 'sec3_3', 'sec3_4','sec3_5', 'sec3_6', 'sec3_7'])
print(Fcols4.describe())

'''*------------------ D1. Table 21, column 2 ------------------*'''
dfBaseline = pd.io.stata.read_stata(r'/Users/gopaljuneja/Desktop/Microenterprise_Kenya/113714-V1/App2017-0042_data/datasets/BDJ_Baseline_Data.dta')
dfBaseline.to_csv('/Users/gopaljuneja/Desktop/Reproduced_MEK/BDJ_Baseline_data.csv')
pd.read_csv(r'/Users/gopaljuneja/Desktop/Reproduced_MEK/BDJ_Baseline_data.csv', index_col = 0)

#Describe sec0, sec1, sec2, sec3
Fcols5 = dfBaseline.filter(items =['sec0','sec1','sec2', 'sec3'])
print(Fcols5.describe())

'''*------------------------------------------------------------------------------------------------------------------------------------------------------------------------*'''

'''D2. Fixed Effects for pooled profit regressions'''
dfDandora = pd.io.stata.read_stata(r'/Users/gopaljuneja/Desktop/Microenterprise_Kenya/113714-V1/App2017-0042_data/datasets/BDJ_Dandora_Data.dta')
dfDandora.to_csv('/Users/gopaljuneja/Desktop/Reproduced_MEK/BDJ_Dandora_data.csv')

dfDandora_rdfcopy = RDataFrame.from_csv('/Users/gopaljuneja/Desktop/Reproduced_MEK/BDJ_Dandora_data.csv')
dfDandora_rdfcopy.xtset(i='id', t='wave')
dfDandora_rdfcopy.fillna(dfDandora_rdfcopy.mean(), inplace = True)

regress_xt = dfDandora_rdfcopy.xtreg('tprofits ~ C(treat) + C(wave)', 'fe', cluster='id')


print(colored('\n HO: mentor = class p-value = \n', 'red'), ft_treat_j.pvalue.item())


dfDandora_dfcopy = dfDandora.copy()
dfDandora_dfcopy = dfDandora_dfcopy.set_index(['id', 'wave'])
dfDandora_dfcopy.fillna(dfDandora_dfcopy.mean(), inplace = True)
dfDandora_dfcopy = dfDandora_dfcopy.drop(columns=['wave_old'])
dfDandora_dfcopy['wave_old'] = dfDandora['wave'].values
dfDandora_dfcopy['id_old'] = dfDandora['id'].values


hypotheses1 = '(C(treat)[T.3.0]  = C(treat)[T.4.0])'
f_test1 = regress.f_test(hypotheses1)

'''-----------* Panel B, Table 22: no controls'''

panel2 = dfDandora.filter(['treat', 'wave','lage_b','secondaryedu_b','sec0_b', 'sec1_b', 'sec2_b', 'sec3_b', 'sec4_b', 'I_emp_b', 'tprofits_b', 'treat2', 'tprofits'], axis=1).astype(float)

formula = "tprofits ~ C(treat) + C(wave)"
reg = smf.ols(formula, dfDandora, missing = 'drop').fit()

#qui test -b[4.treat] = _b[3.treat]
hypotheses = '(C(treat)[T.3.0]  = C(treat)[T.4.0])'
f_test = reg.f_test(hypotheses)
#extracting the p-value from the f_test
f_test.pvalue.item()
print(reg.summary())
print(colored('HO: mentor = class p-value = ', 'red'), f_test.pvalue.item())
print(colored('hello', 'red'), colored('world', 'green'))




