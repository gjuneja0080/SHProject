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
df_panelData = df_BDJ_Dandora.filter(['id', 'wave','profit_b','businessage_b','I_emp_b', 'emp_b', 'credit_b', 'bankaccount_b', 'loan_b', 'formalaccount_b', 'advert_b', 'manu_b', 'retail_b', 'food_b', 'serv_b', 'age_b', 'secondaryedu_b', 'treat2'], axis=1).astype(float)
df_panelData = df_panelData.set_index(['id', 'wave'])

panel = df_panelData.xs(0, level = 'wave')

#Transfer categorical variables to dummy variables
preTreat2Factors = pd.get_dummies(panel['treat2'], prefix='treat2')

#To eliminate multicollinearity, delete one of the factor variables
treat2Factor = dummyTreat.drop(['treat2_2.0'], axis = 'columns')

#Join panel balancelist with the dummy variables
panelFactor = pd.concat([panel, dummyTreat], axis = 'columns')

def OLSregression(x):
    formula = "%s ~ treat2Factor" % x
    formalaccount_b = smf.ols(formula, panelFactor).fit()
    return formalaccount_b.summary()


#Baseline Balance: profit_b
OLSregression('profit_b')

#Baseline Balance: businessage_b
OLSregression('businessage_b')

#Baseline Balance: I_emp_b
OLSregression('I_emp_b')

#Baseline Balance: emp_b
OLSregression('emp_b')

#Baseline Balance: credit_b
OLSregression('credit_b')

#Baseline Balance: bankaccount_b
OLSregression('bankaccount_b')

#Baseline Balance: loan_b
OLSregression('loan_b')

#Baseline Balance: formalaccount_b
OLSregression('formalaccount_b')

#Baseline Balance: advert_b
OLSregression('advert_b')

#Baseline Balance: 'manu_b'
OLSregression('manu_b')

#Baseline Balance: 'retail_b'
OLSregression('retail_b')

#Baseline Balance: 'food_b'
OLSregression('food_b')

#Baseline Balance: 'serv_b'
OLSregression('serv_b')

#Baseline Balance: 'age_b'
OLSregression('age_b')

#Baseline Balance: 'secondaryedu_b'
OLSregression('secondaryedu_b')
