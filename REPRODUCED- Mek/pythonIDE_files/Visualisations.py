#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 23:21:09 2020

@author: gopaljuneja
"""

import pandas as pd
from termcolor import colored
import numpy as np
import warnings
%matplotlib inline
import statsmodels.formula.api as smf
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor    
import statistics
'''MainTables.do'''

dfDandora = pd.io.stata.read_stata(r'/Users/gopaljuneja/Desktop/Microenterprise_Kenya/113714-V1/App2017-0042_data/datasets/BDJ_Dandora_Data.dta')
dfDandora.to_csv('/Users/gopaljuneja/Desktop/Reproduced_MEK/BDJ_Dandora_data.csv')




'''* ---------------- Figure 3: average profit timeseries graph ------------------------- *'''

dfDandora_sort = dfDandora.sort_values(['treat2', 'wave'], ascending=[True, True])
dfDandora_sort.wave.describe()

dfDandora_sort = dfDandora_sort.append({'months_since_treat': -1, 'treat' : 2}, ignore_index=True)
dfDandora_sort = dfDandora_sort.append({'months_since_treat': -1, 'treat' : 3}, ignore_index=True)
dfDandora_sort = dfDandora_sort.append({'months_since_treat': -1, 'treat' : 4}, ignore_index=True)
dfDandora_sort = dfDandora_sort.append({'months_since_treat': 0, 'treat' : 2}, ignore_index=True)
dfDandora_sort = dfDandora_sort.append({'months_since_treat': 0, 'treat' : 3}, ignore_index=True)
dfDandora_sort = dfDandora_sort.append({'months_since_treat': 0, 'treat' : 4}, ignore_index=True)

dfDandora_sort['shade'] = 0
dfDandora_sort.loc[dfDandora_sort['months_since_treat'] == -1, 'shade'] = 3500
dfDandora_sort.loc[dfDandora_sort['months_since_treat'] == 0, 'shade'] = 3500

lst = ["treat2", "months_since_treat","shade"]
avg_profits = dfDandora_sort.groupby(lst, axis = 0)["tprofits"].agg(['mean'])

avg_profits = avg_profits.sort_values(['months_since_treat'], ascending=[True])


avg_profits.to_csv('/Users/gopaljuneja/Desktop/Reproduced_MEK/Fig3.csv')

'''* ---------------- Figure 6: fraction still meeting with mentors ------------------------- *'''

sortWave = dfDandora_sort.sort_values(['wave'], ascending = [True])
dfDandora_sort.months_since_treat.unique()
dfDandora_sort.loc[dfDandora_sort['months_since_treat'] == 0]
lst1 = ['wave', 'months_since_treat']
avg_meet = sortWave.groupby(lst1, axis =0)["meet"].agg(['mean']).reset_index()
#2000 is a substitue for '.' in the original paper due to value error being thrown 
sortWave.loc[sortWave['wave'] == 7, 'months_since_treat'] = np.nan

sortWave.loc[sortWave['months_since_treat'] < 0, 'months_since_treat'] = np.nan

sortWave = sortWave.append({'months_since_treat': 0}, ignore_index=True)
sortWave['months_since_treat'].value_counts()

avg_meet.loc[avg_meet['months_since_treat'] == 0, 'mean'] = 1

avg_meet = avg_meet.sort_values(['months_since_treat'], ascending = [True])

avg_meet.to_csv('/Users/gopaljuneja/Desktop/Reproduced_MEK/Fig6.csv')

'''* --------- Figure 7: Profit for those that meet and those that don't' --------- *'''

dfcopy = sortWave.copy()
del dfcopy['treat2']

dfcopy['treat2'] = dfcopy['treat']

dfcopy.loc[(dfcopy['treat'] == 4) & (dfcopy['meet'] == 1) , 'treat2'] = 5
dfcopy.wave.value_counts()

dfcopy['treat2'].value_counts()
#sort by treat2, wave
sortbyVar = dfcopy.sort_values(['treat2','wave'], ascending = [True, True])
lst3 = ['treat2', 'wave','months_since_treat']
avg_profitm2 = sortbyVar.groupby(lst3, axis = 0)["tprofits"].agg(['mean']).reset_index()

sortbyVar = sortbyVar.append({'months_since_treat': 0, 'treat2' : 2}, ignore_index=True)
sortbyVar = sortbyVar.append({'months_since_treat': 0, 'treat2' : 3}, ignore_index=True)
sortbyVar = sortbyVar.append({'months_since_treat': 0, 'treat2' : 4}, ignore_index=True)
sortbyVar = sortbyVar.append({'months_since_treat': 0, 'treat2' : 5}, ignore_index=True)
avg_profitm2 = avg_profitm2.sort_values(['months_since_treat'], ascending = [True])
avg_profitm2 = avg_profitm2.drop(avg_profitm2[(avg_profitm2.treat2 < 4)].index)

avg_profitm2.to_csv('/Users/gopaljuneja/Desktop/Reproduced_MEK/Fig7.csv')

'''* --------- Figure 1 (uses baseline data)'''
dfBaseline = pd.io.stata.read_stata(r'/Users/gopaljuneja/Desktop/Microenterprise_Kenya/113714-V1/App2017-0042_data/datasets/BDJ_Baseline_Data.dta')
dfBaseline.to_csv('/Users/gopaljuneja/Desktop/Reproduced_MEK/BDJ_Baseline_data.csv')

baselineFiltered = dfBaseline[(dfBaseline.youngfirm == 0)]
ax = baselineFiltered['lprofit'].plot.kde(bw_method = 0.15)

'''* ----------- Figure 2 (uses baseline data)'''
baselineFiltered1 = dfBaseline.filter(items=['binf', 'gender', 'bf', 'avg_profit_agegen'])
baselineFiltered1 = baselineFiltered1.sort_values(['bf'], ascending = [True])
#drop if current value is the same as the previous one
baselineFiltered1 = baselineFiltered1[baselineFiltered1['bf'] != baselineFiltered1['bf'].shift(-1)]
baselineFiltered1 = baselineFiltered1.dropna() 
baselineFiltered1['binf'] = baselineFiltered1.binf.astype(int)
baselineFiltered1 = baselineFiltered1.assign(c3 = baselineFiltered1.groupby('binf')['gender'].rank()).sort_values(['gender', 'binf']).drop('c3', axis=1)

baselineFiltered1['_hold'] = np.nan

baselineFiltered1.loc[baselineFiltered1['binf'] == 1, '_hold'] = baselineFiltered1.avg_profit_agegen
baselineFiltered1['_hold2'] = np.where(baselineFiltered1['gender'] == 0, '15480.3','9295.81')
baselineFiltered1['avg_profit_agegen_norm'] = baselineFiltered1.avg_profit_agegen.astype(float) / baselineFiltered1._hold2.astype(float)

ages = ["0-1", "1-5", "5-10", "10-15", "15-20",">20", "0-1", "1-5", "5-10", "10-15", "15-20",">20"]
baselineFiltered1['Business Experience(years)'] = ages
baselineFiltered1 = baselineFiltered1.drop(['_hold','_hold2'], axis = 1)

baselineFiltered1.to_csv('/Users/gopaljuneja/Desktop/Reproduced_MEK/Fig2.csv')



'''Appendix.do'''

'''* ------- APPENDIX B: Baseline Learning Methods'''
dfBaseline = pd.io.stata.read_stata(r'/Users/gopaljuneja/Desktop/Microenterprise_Kenya/113714-V1/App2017-0042_data/datasets/BDJ_Baseline_Data.dta')

filterBaseline = dfBaseline.sort_values(['bl'], ascending = [True])
filterBaseline = filterBaseline[filterBaseline['bl'] != filterBaseline['bl'].shift(-1)]
filterBaseline = filterBaseline.set_value(1, 'binl', 0)
filterBaseline = filterBaseline.drop(filterBaseline.index[0])
ages1 = ["<1", "1-5", "5-10", "10-15", ">15", "<1", "1-5", "5-10", "10-15", ">15"]
filterBaseline['Business Experience(years)'] = ages1
filterBaseline = filterBaseline.filter(items=['self_taught', 'binl', 'bl', 'avg_I_emp_learn', 'lavg_profit_learn', 'lavg_wagebill_learn','Business Experience(years)'])
filterBaseline.to_csv('/Users/gopaljuneja/Desktop/Reproduced_MEK/Fig8.csv')

