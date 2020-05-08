#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 16:09:42 2020

@author: gopaljuneja
"""
import pandas as pd
from termcolor import colored
import numpy as np
import warnings
import statsmodels.formula.api as smf
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor    
import statistics


dfBaseline = pd.io.stata.read_stata(r'/Users/gopaljuneja/Desktop/Microenterprise_Kenya/113714-V1/App2017-0042_data/datasets/BDJ_Baseline_Data.dta')
dfBaseline.to_csv('/Users/gopaljuneja/Desktop/Reproduced_MEK/BDJ_Baseline_data.csv')

dfDandora = pd.io.stata.read_stata(r'/Users/gopaljuneja/Desktop/Microenterprise_Kenya/113714-V1/App2017-0042_data/datasets/BDJ_Dandora_Data.dta')
dfDandora.to_csv('/Users/gopaljuneja/Desktop/Reproduced_MEK/BDJ_Dandora_data.csv')

dfRD_Dataset = pd.io.stata.read_stata(r'/Users/gopaljuneja/Desktop/Microenterprise_Kenya/113714-V1/App2017-0042_data/datasets/RD_Dataset.dta')
dfRD_Dataset.to_csv('/Users/gopaljuneja/Desktop/Reproduced_MEK/RD_Dataset.csv')
 
df = dfBaseline[['tprofit','businessage','employees', 'employeesnumber', 'credit', 'bankaccount', 'loan', 'account', 'marketing', 'age', 'gender', 'secondaryedu']].describe()

df.describe()
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


df_Baseline_metrics = getStats(dfBaseline)

#replace employeesnumber = 0 if employees = 0
if(dfBaseline.employees.any() == 0):
    dfBaseline.employeesnumber = 0
    
new_BDJ_Dandora = dfDandora.filter(['profit_b','businessage_b','I_emp_b', 'emp_b', 'credit_b', 'bankaccount_b', 'loan_b', 'formalaccount_b', 'advert_b', 'manu_b', 'retail_b', 'food_b', 'serv_b', 'age_b', 'secondaryedu_b'], axis=1).astype(float)

#Creating xtset panel data and extracting local balancelist
df_panelData = dfDandora.copy()
df_panelData = dfDandora.filter(['id', 'wave','profit_b','businessage_b','I_emp_b', 'emp_b', 'credit_b', 'bankaccount_b', 'loan_b', 'formalaccount_b', 'advert_b', 'manu_b', 'retail_b', 'food_b', 'serv_b', 'age_b', 'secondaryedu_b', 'treat2'], axis=1).astype(float)
df_panelData = df_panelData.set_index(['id', 'wave'])

panel = df_panelData.xs(0, level = 'wave')

#Transfer categorical variables to dummy variables
preTreat2Factors = pd.get_dummies(panel['treat2'], prefix='treat2')

#To eliminate multicollinearity, delete one of the factor variables
treat2Factor = preTreat2Factors.drop(['treat2_2.0'], axis = 'columns')

#Join panel balancelist with the dummy variables
panelFactor = pd.concat([panel, treat2Factor], axis = 'columns')

def OLSregression(x):
    formula = "%s ~ C(treat2)" % x
    regress = smf.ols(formula, panel).fit()
    return regress.summary()

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

'''*-----------------------Table 3: baseline profit regressions-----------------------*'''

#----- VARIABLE: PROFIT ... WAVE = POOLED ... CONTROLS = YES -----

#reg tprofits i.treat i.wave $controls tprofits_b if wave>=0 & wave<=7


# NOTE :: Wave for every row is in between 0 and 7

panel2 = dfDandora.filter(['treat', 'wave','lage_b','secondaryedu_b','sec0_b', 'sec1_b', 'sec2_b', 'sec3_b', 'sec4_b', 'I_emp_b', 'tprofits_b', 'treat2', 'tprofits'], axis=1).astype(float)

formula = "tprofits ~ C(treat) + C(wave) + tprofits_b + lage_b + secondaryedu_b + sec0_b + sec1_b + sec2_b + sec3_b + sec4_b + I_emp_b"
reg = smf.ols(formula, panel2, missing = 'drop').fit()

#qui test -b[4.treat] = _b[3.treat]
hypotheses = '(C(treat)[T.3.0]  = C(treat)[T.4.0])'
f_test = reg.f_test(hypotheses)
#extracting the p-value from the f_test
f_test.pvalue.item()
reg.summary()
print(colored('HO: mentor = class p-value = ', 'red'), f_test.pvalue.item())
print(colored('hello', 'red'), colored('world', 'green'))


for i in range(1,8):
    print(colored('VARIABLE: PROFIT ... WAVE = {} ... CONTROLS = YES -----'.format(i), 'red'), sep = '\n')
    df_waveFilter = panel2.loc[(panel2['wave'] == i)]
    formula1 = "tprofits ~ C(treat) + wave + tprofits_b + lage_b + secondaryedu_b + sec0_b + sec1_b + sec2_b + sec3_b + sec4_b + I_emp_b"
    regress = smf.ols(formula1, df_waveFilter, missing = 'drop').fit()
    hypotheses1 = '(C(treat)[T.3.0]  = C(treat)[T.4.0])'
    f_test1 = regress.f_test(hypotheses1)
    print(regress.summary())
    print(colored('\nHO: mentor = class p-value = ', 'red'), f_test1.pvalue.item())
    print('\n')

'''--------Table 4: Hetergenous Effects----------'''    

dfDandora['class_'] = dfDandora['class']
dfDandora['id_'] = dfDandora['id']
# rename 'class' and 'id' column to avoid conflict with python's built in class and id functions


filterBDJD = dfDandora.filter(['tprofits', 'class_', 'mentorL', 'mentorM', 'mentorH', 'wave', 'tprofits_b','id_'], axis =1).astype(float)
dfDandora.fillna(dfDandora.mean(), inplace = True)
formulaHeteroE = "tprofits ~ class_ + mentorL + mentorM + mentorH + C(wave) + tprofits_b + lage_b + secondaryedu_b + sec0_b + sec1_b + sec2_b + sec3_b + sec4_b + I_emp_b"
regressHeteroE = smf.ols(formulaHeteroE, dfDandora, missing = 'drop').fit(cov_type='cluster',cov_kwds={'groups': dfDandora['id_']}, use_t = True)
regressHeteroE.summary()

dummyPanel = pd.get_dummies(dfDandora['wave'], prefix = 'wave')
dummyPanel = dummyPanel.drop(['wave_0.0', 'wave_1.0', 'wave_2.0', 'wave_3.0'], axis=1)



'''------Table6---------'''

dfDandora_copy = dfDandora.copy()

wavePanel = pd.get_dummies(dfDandora['wave'], prefix = 'wave')
wavePanel = wavePanel.drop(['wave_0.0', 'wave_1.0', 'wave_2.0', 'wave_3.0'], axis=1)

treatPanel = pd.get_dummies(dfDandora['treat'], prefix = 'treat')
treatPanel = treatPanel.drop(['treat_2.0'], axis=1)

dfDandora_copy = pd.concat([dfDandora_copy,wavePanel,treatPanel], axis = 'columns')
dfDandora_copy = dfDandora_copy.rename(columns={"treat_3.0":"treat_3", "treat_4.0":"treat_4", "wave_4.0": "wave_4", "wave_5.0": "wave_5", "wave_6.0": "wave_6", "wave_7.0": "wave_7"})
dfDandora_copy = dfDandora_copy.set_index(['id', 'wave'])

dfDandora_copy['id'] = dfDandora.id.values

print(colored('Table 6: VARIABLE: REVENUE .... CONTROLS = NO ------', 'red'), sep = '\n')
fml1 = "trevenue ~ treat_3 + treat_4 + wave_4 + wave_5 + wave_6 + wave_7 - 1"

dfDandora_copy.fillna(dfDandora_copy.mean(), inplace = True)
reg = smf.ols(fml1, dfDandora_copy, missing = 'drop').fit(cov_type='cluster',cov_kwds={'groups': dfDandora_copy['id']}, use_t = True)

'''############################################################################################################################################################################'''

cols = ['keeps_some_records', 'marketing']
for i in cols:
    print(colored("----------Table 11. Variable: {} ....... WAVE = POOLED .... CONTROLS = YES".format(i), "red"))
    df_filterWave =  dfDandora[dfDandora['wave'].between(1, 6)]
    df_filterWave.fillna(df_filterWave.mean(), inplace = True)
    fml_i = "{} ~ C(treat) + C(wave) + lage_b + secondaryedu_b + sec0_b + sec1_b + sec2_b + sec3_b + sec4_b + I_emp_b ".format(i)
    regress_i = smf.ols(fml_i, df_filterWave).fit(cov_type='cluster',
                                                        cov_kwds={'groups': df_filterWave['id']}, use_t = True)
    treatComp = '(C(treat)[T.4.0] = C(treat)[T.3.0])'
    ft_treat_i = regress_i.f_test(treatComp)
    
    print(regress_i.summary())
    print(colored('\n HO: mentor = class p-value = ', 'red'), ft_treat_i.pvalue.item())
    
    for j in range(1,7):
        print(colored("\n----- TABLE 11. VARIABLE: `{}' ... WAVE = {} ... CONTROLS = YES -----\n".format(i, j), "red"))
        regression_formula = "{} ~ C(treat) + lage_b + secondaryedu_b + sec0_b + sec1_b + sec2_b + sec3_b + sec4_b + I_emp_b ".format(i)
        
        df = df_filterWave.loc[(df_filterWave['wave'] == j)]
        df.fillna(df.mean(), inplace = True)
        
        regress_j = smf.ols(regression_formula, df).fit()
        ft_treat_j = regress_j.f_test(treatComp)
        
        print(regress_j.summary())
        print(colored('\n HO: mentor = class p-value = \n', 'red'), ft_treat_j.pvalue.item())
    
dfDandora.z_marketing_score.isna().all()
dfDandora.z_business_score.isna().all()

practicevec2 = ["z_business_score","z_marketing_score", "z_stock_score", "z_record_score" ]
for x in practicevec2:
    print(colored("\n----- TABLE 12. VARIABLE: {} ... WAVE = 5+6 ... CONTROLS = YES -----\n".format(x), "red"))
    df_filterDandora = dfDandora[dfDandora['wave'].between(5,6)]
    fml_x = "{} ~ C(treat) + C(wave) + lage_b + secondaryedu_b + sec0_b + sec1_b + sec2_b + sec3_b + sec4_b + I_emp_b".format(x)
    regress_x =  smf.ols(fml_x, df_filterDandora).fit(cov_type='HC1', use_t = True)
    
    treatComp = '(C(treat)[T.4.0] = C(treat)[T.3.0])'
    ft_treat_x = regress_x.f_test(treatComp)
    
    df_filterbyTreatment = df_filterDandora.loc[(df_filterDandora['treat'] == 2)].describe()
    
    print(regress_x.summary())
    print(colored('\n HO: mentor = class p-value = ', 'red'), ft_treat_x.pvalue.item())
    
    stdev_val = regress_x.bse
    treatmentstdev = stdev_val.iloc[1]
    treatmentstdev2 = stdev_val.iloc[2]
    averagetreatment = (treatmentstdev + treatmentstdev2)/2
    
    print(colored("\n Treatment StandardDev = ", 'red'), averagetreatment)



dfDandora_sorted = dfDandora.sort_values(["treat2", "wave"], ascending = (True))
lst = ["treat2", "wave"]
dfDandora_sorted.groupby(lst, axis = 0)["tprofits"].agg(['mean'])
dfDandora_sorted.wave.describe()

df_filterDandora = dfDandora[dfDandora['wave']== 5]


dfDandora_sorted = dfDandora_sorted.append({'months_since_treat': -1, 'treat' : 2}, ignore_index=True)
dfDandora_sorted = dfDandora_sorted.append({'months_since_treat': -1, 'treat' : 3}, ignore_index=True)
dfDandora_sorted = dfDandora_sorted.append({'months_since_treat': -1, 'treat' : 4}, ignore_index=True)
dfDandora_sorted = dfDandora_sorted.append({'months_since_treat': 0, 'treat' : 2}, ignore_index=True)
dfDandora_sorted = dfDandora_sorted.append({'months_since_treat': 0, 'treat' : 3}, ignore_index=True)
dfDandora_sorted = dfDandora_sorted.append({'months_since_treat': 0, 'treat' : 4}, ignore_index=True)


dfDandora_sorted['shade'] = [3500 if x >=-1 and x<=0 
                     else dfDandora_sorted.fillna(0) 
                     for x in dfDandora_sorted['months_since_treat']]


for i,j in enumerate(dfDandora_sorted['months_since_treat']):
    if(j == -1.0):
        dfDandora_sorted['shade']= 3500
    elif(j == 0.0):
        dfDandora_sorted['shade'] = 3500




dfSplit1 = dfDandora_sorted.loc[dfDandora_sorted['months_since_treat'] == 0.0]
dfSplit2 = dfDandora_sorted.loc[dfDandora_sorted['months_since_treat'] == -1.0]
dfShade = pd.concat([dfSplit1, dfSplit2])
dfShade['shade'] = 3500

dfSplit3 = dfDandora_sorted.loc[dfDandora_sorted['months_since_treat'] > 0.0]
dfSplit4 = dfDandora_sorted.loc[dfDandora_sorted['months_since_treat'] < -1.0]
dfNoshade = pd.concat([dfSplit3, dfSplit4])
dfNoshade['shade'] = 0

df_shadedDandora = pd.concat([dfShade,dfNoshade])
df_shadedDandora.to_csv('/Users/gopaljuneja/Desktop/Reproduced_MEK/df_shadedDandora_sorted.csv')

dfDandora_sorted.dtypes
dfDandora_sorted.head()
dfDandora_sorted = dfDandora_sorted.sort_values(["shade"], ascending = (True))

#drop columns
dfDandora_sorted = dfDandora_sorted.drop('shade', axis = 1)
#To drop rows
dfDandora_sorted = dfDandora_sorted[:-1]

dfDandora.supplierswitch.isna().sum()



'''--------Table 5: Regression Discontinuity on Mentors----------'''

from rdd import rdd


N = 10000
x = np.random.normal(1, 1, N)
epsilon = np.random.normal(0, 1, N)
threshold = 1
treatment = np.where(x >= threshold, 1, 0)
w1 = np.random.normal(0, 1, N)
w2 = np.random.normal(0, 4, N)
y = .5 * treatment + 2 * x - .2 * w1 + 1 + epsilon

data = pd.DataFrame({'y':y, 'x': x, 'w1':w1, 'w2':w2})
data.head()


bandwidth_opt = rdd.optimal_bandwidth(data['y'], data['x'], cut=threshold)


print("Optimal bandwidth:", bandwidth_opt)
data_rdd = rdd.truncated_data(data, 'x', bandwidth_opt, cut=threshold)

#x = running variable
#y = outcome variables
model = rdd.rdd(data_rdd, 'x', 'y', cut=threshold)
print(model.fit().summary())


df_RD = pd.io.stata.read_stata(r'/Users/gopaljuneja/Desktop/Microenterprise_Kenya/113714-V1/App2017-0042_data/datasets/RD_Dataset.dta')
df_RD.to_csv('/Users/gopaljuneja/Desktop/Reproduced_MEK/RD_Dataset.csv')


bw100 = 100
bw150 = 150
bw200 = 200
threshold = 1
rdd.optimal_bandwidth()

band100 = df_RD.loc[(df_RD['ce_std'] <= 1) & (df_RD['ce_std'] >= -1 * 1)]
band150 = df_RD.loc[(df_RD['ce_std'] <= 1.5) & (df_RD['ce_std'] >= -1 * 1.5)]
band200 = df_RD.loc[(df_RD['ce_std'] <= 2) & (df_RD['ce_std'] >= -1 * 2)]



bandwidth_optimal = rdd.optimal_bandwidth(df_RD['tprofit_endline'], df_RD['ce_std'], cut=threshold)

bandwidth_optimal = rdd.optimal_bandwidth(band150['tprofit_endline'], band150['ce_std'], cut=threshold)
bandwidth_optimal = rdd.optimal_bandwidth(band200['tprofit_endline'], band200['ce_std'], cut=threshold)
bandwidth_optimal = rdd.optimal_bandwidth(band100['tprofit_endline'], band100['ce_std'], cut=threshold)


model1 = rdd.rdd(df_RD, 'ce_std', 'tprofit_endline', cut = threshold)
print(model1.fit().summary())

