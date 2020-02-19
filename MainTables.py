#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 16:09:42 2020

@author: gopaljuneja
"""
import pandas as pd
import numpy as np
%matplotlib inline
import statsmodels.formula.api as smf
import statsmodels.api as sm


df_BDJ_Baseline = pd.io.stata.read_stata(r'/Users/gopaljuneja/Desktop/Microenterprise_Kenya/113714-V1/App2017-0042_data/datasets/BDJ_Baseline_Data.dta')
df_BDJ_Baseline.to_csv('/Users/gopaljuneja/Desktop/Reproduced_MEK/BDJ_Baseline_data.csv')
pd.read_csv(r'/Users/gopaljuneja/Desktop/Reproduced_MEK/BDJ_Baseline_data.csv')

df_BDJ_Dandora = pd.io.stata.read_stata(r'/Users/gopaljuneja/Desktop/Microenterprise_Kenya/113714-V1/App2017-0042_data/datasets/BDJ_Dandora_Data.dta')
df_BDJ_Dandora.to_csv('/Users/gopaljuneja/Desktop/Reproduced_MEK/BDJ_Dandora_data.csv')
pd.read_csv(r'/Users/gopaljuneja/Desktop/Reproduced_MEK/BDJ_Dandora_data.csv')

df_RD_Dataset = pd.io.stata.read_stata(r'/Users/gopaljuneja/Desktop/Microenterprise_Kenya/113714-V1/App2017-0042_data/datasets/RD_Dataset.dta')
df_RD_Dataset.to_csv('/Users/gopaljuneja/Desktop/Reproduced_MEK/RD_Dataset.csv')
pd.read_csv(r'/Users/gopaljuneja/Desktop/Reproduced_MEK/RD_Dataset.csv')


#extracting rows from df_BDJ_Baseline where youngfirm = 1

temp = df_BDJ_Baseline.loc[(df_BDJ_Baseline['youngfirm'] == 1)]


df = df_BDJ_Baseline[['tprofit','businessage','employees', 'employeesnumber', 'credit', 'bankaccount', 'loan', 'account', 'marketing', 'age', 'gender', 'secondaryedu']].describe()

def getStats(df):
    df_a = pd.DataFrame(index = ['tprofit','businessage','employees', 'employeesnumber', 'credit', 'bankaccount', 'loan', 'account', 'marketing', 'age', 'gender', 'secondaryedu' ], columns = ['Obs', 'Mean', 'Std.Dev', 'Min', 'Max']).astype(float)
    
    #creating a list of the columns required
    colist = ['tprofit','businessage','employees', 'employeesnumber', 'credit', 'bankaccount', 'loan', 'account', 'marketing', 'age', 'gender', 'secondaryedu']
    
    #selecting the columns where youngfirm = 1
    df = df.loc[(df['youngfirm'] == 1)]
    
    for i,j in enumerate(colist):
        df_a.ix[i,'Obs']= df[j].count()
        df_a.ix[i,'Mean']= df[j].mean()
        df_a.ix[i,'Std.Dev']= df[j].std()
        df_a.ix[i,'Min']= df[j].min()
        df_a.ix[i,'Max']= df[j].max()
    return df_a


df_Baseline_metrics = getStats(df_BDJ_Baseline)

#replace employeesnumber = 0 if employees = 0
if(df_BDJ_Baseline.employees.any() == 0):
    df_BDJ_Baseline.employeesnumber = 0
    
new_BDJ_Dandora = df_BDJ_Dandora.filter(['profit_b','businessage_b','I_emp_b', 'emp_b', 'credit_b', 'bankaccount_b', 'loan_b', 'formalaccount_b', 'advert_b', 'manu_b', 'retail_b', 'food_b', 'serv_b', 'age_b', 'secondaryedu_b'], axis=1).astype(float)

#Creating xtset panel data and extracting local balancelist
df_panelData = df_BDJ_Dandora.copy()
df_panelData = df_BDJ_Dandora.filter(['id', 'wave','profit_b','businessage_b','I_emp_b', 'emp_b', 'credit_b', 'bankaccount_b', 'loan_b', 'formalaccount_b', 'advert_b', 'manu_b', 'retail_b', 'food_b', 'serv_b', 'age_b', 'secondaryedu_b'], axis=1).astype(float)
df_panelData = df_panelData.set_index(['id', 'wave'])




