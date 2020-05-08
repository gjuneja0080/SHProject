#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 04:14:38 2020

@author: gopaljuneja
"""

import pandas as pd
import numpy as np
import warnings
import statsmodels.formula.api as smf
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor    
import statistics
import array as arr

df_BDJDandora = pd.io.stata.read_stata(r'/Users/gopaljuneja/Desktop/Microenterprise_Kenya/113714-V1/App2017-0042_data/datasets/BDJ_Dandora_Data.dta')
dfDandora = df_BDJDandora.copy()

dfDandora = dfDandora.set_index(['id', 'wave'])
dfDandora['wave'] = df_BDJDandora['wave'].values
dfDandora['id'] = df_BDJDandora['id'].values
dfDandora = dfDandora.rename(columns={"wave": "Lwave", "id": "Lid"})


'''How persistent are problems?'''

dfDandora = dfDandora[dfDandora['Lwave'].isin([5, 0])]
dfDandora['Lwave'].value_counts()
dfDandora['treat'] = dfDandora['treat2'].values
dfDandora = dfDandora.drop(['treat2'], axis = 1)

countdf = dfDandora.groupby('Lid').count()
result = dfDandora.loc[dfDandora['Lid'].isin(countdf[countdf['Lwave'] > 1].index)]
arr = result.Lid.value_counts()
arr.value_counts()
dfDandora = result.copy()
lst = ['treat','id','wave']
dfDandora = dfDandora.sort_values(lst, ascending = [True, True, True])

#get a list of all columns
cols = list(dfDandora)
# move the column to head of list using index, pop and insert
cols.insert(0, cols.pop(cols.index('treat')))
dfDandora = dfDandora.loc[:, cols] 

dfDandora = dfDandora.sort_values(lst, ascending = [True, True, True])
toughx = dfDandora['difficulties'].str.split(' ', expand = True)
toughx[0] = pd.to_numeric(toughx[0], errors='coerce')
toughx[1] = pd.to_numeric(toughx[1], errors='coerce')
toughx[2] = pd.to_numeric(toughx[2], errors='coerce')
toughx[3] = pd.to_numeric(toughx[3], errors='coerce')
toughx[4] = pd.to_numeric(toughx[4], errors='coerce')

toughx[4].value_counts()
toughx = toughx.rename(columns={0: "tough1", 1: "tough2", 2: "tough3", 3: "tough4", 4: "tough5"})
combined = pd.concat([dfDandora, toughx], axis=1)
dfDandora = combined.copy()
dfDandora = dfDandora.sort_values(['Lid','Lwave'], ascending = [True, True])

backup = dfDandora.copy()

for i in range(0, 12):
    backup['istough_{}'.format(i)] = 0
    backup.loc[(backup['tough1'] == i) | 
            (backup['tough2'] == i) | 
            (backup['tough3'] == i) | 
            (backup['tough4'] == i) | 
            (backup['tough5'] == i) , 'istough_{}'.format(i)] = 1
    backup['_hold'] = np.where((backup.Lwave == 0), backup['istough_{}'.format(i)].values, np.nan)
    backup['istough0_{}'.format(i)] = backup.groupby(['Lid'], axis = 0)['_hold'].transform('max')
    backup = backup.drop(['_hold'], axis = 1)
    
    backup['_hold'] = np.where((backup.Lwave == 5), backup['istough_{}'.format(i)].values, np.nan)
    backup['istough5_{}'.format(i)] = backup.groupby(['Lid'], axis = 0)['_hold'].transform('max')
    backup = backup.drop(['_hold'], axis = 1)

lst = ['istough_0', 'istough_1', 'istough_2','istough_3', 'istough_4', 'istough_5', 'istough_6', 'istough_7', 'istough_8', 'istough_9', 'istough_10', 'istough_11' ]
backup = backup.drop(lst, axis = 1)


dfDandora = backup.copy()
dfDandora = dfDandora.sort_values(['Lid'], ascending = [True])

dfDandora = dfDandora[dfDandora['Lid'] != dfDandora['Lid'].shift(-1)]

lst1 = ['difficulties', 'Lwave', 'tough1', 'tough2', 'tough3', 'tough4', 'tough5']
dfDandora = dfDandora.drop(lst1, axis = 1)

backup = dfDandora.copy()

for i in range(0,12):
    backup['new_{}'.format(i)] = 0
    backup.loc[(backup['istough0_{}'.format(i)] == 0) & (backup['istough5_{}'.format(i)] == 1) , 'new_{}'.format(i)] = 1
    backup.loc[(backup['istough0_{}'.format(i)] != 0), 'new_{}'.format(i)] = np.nan
    
    backup['dropped_{}'.format(i)] = 0
    backup.loc[(backup['istough0_{}'.format(i)] == 0) & (backup['istough5_{}'.format(i)] == 1) , 'dropped_{}'.format(i)] = 1
    backup.loc[(backup['istough0_{}'.format(i)] != 0), 'dropped_{}'.format(i)] = np.nan
    
dfDandora = backup.copy()


probs0 = dfDandora.filter(items = ['istough0_0', 'istough0_1', 'istough0_2','istough0_3', 'istough0_4', 'istough0_5', 'istough0_6', 'istough0_7', 'istough0_8', 'istough0_9', 'istough0_10', 'istough0_11'])
dfDandora['probs0'] = probs0.sum(axis=1)

probs5 = dfDandora.filter(items = ['istough5_0', 'istough5_1', 'istough5_2','istough5_3', 'istough5_4', 'istough5_5', 'istough5_6', 'istough5_7', 'istough5_8', 'istough5_9', 'istough5_10', 'istough5_11'])
dfDandora['probs5'] = probs5.sum(axis=1)


dfDandora = dfDandora.sort_values(['treat'], ascending = [True])

cols = list(dfDandora)
cols = ['treat','Lid','new_0',
 'new_1',
 'new_2',
 'new_3',
 'new_4',
 'new_5',
 'new_6',
 'new_7',
 'new_8',
 'new_9',
 'new_10',
 'new_11',
 'dropped_0',
 'dropped_1',
 'dropped_2',
 'dropped_3',
 'dropped_4',
 'dropped_5',
 'dropped_6',
 'dropped_7',
 'dropped_8',
 'dropped_9',
 'dropped_10',
 'dropped_11',
 'probs0',
 'probs5',
 'months_since_treat',
 'count',
 'meet',
 'meet2',
 'tprofits',
 'delta_profits',
 'delta_profits_c',
 'delta_profits_b',
 'trevenue',
 'price',
 'cprice',
 'delta_meet',
 'mentorbenefit',
 'discuss',
 'discussever',
 'otherinvest',
 'loanlastyear',
 'marketing',
 'temployeesnumber',
 'I_emp',
 'twagebill',
 'tinventorystock',
 'tweekopen',
 'keeps_some_records',
 'supplierswitch',
 'new_product',
 'z_business_score',
 'z_marketing_score',
 'marketing_score',
 'competitorprice',
 'competitorproduct',
 'sales',
 'upsell',
 'do_advert',
 'z_stock_score',
 'stock_score',
 'supplierhaggle',
 'suppliercompare',
 'stockout',
 'z_record_score',
 'record_score',
 'everysale',
 'consultrecords',
 'budget',
 'class',
 'mentorL',
 'mentorM',
 'mentorH',
 'exit',
 'secondaryedu_M',
 'mentorL_ba',
 'mentorM_ba',
 'mentorH_ba',
 'mentor_hs',
 'mentor_ps',
 'profit_b',
 'tprofits_b',
 'emp_b',
 'emp_b2',
 'I_emp_b',
 'age_b',
 'lage_b',
 'businessage_b',
 'sec0_b',
 'sec1_b',
 'sec2_b',
 'sec3_b',
 'sec4_b',
 'sec0_0',
 'sec0_1',
 'sec0_2',
 'sec0_3',
 'sec0_4',
 'sec0_5',
 'sec0_6',
 'sec0_7',
 'sec0_8',
 'sec0_9',
 'sec0_10',
 'sec1_1',
 'sec1_2',
 'sec1_3',
 'sec1_4',
 'sec1_5',
 'sec1_6',
 'sec2_0',
 'sec2_1',
 'sec2_2',
 'sec2_3',
 'sec2_4',
 'sec2_5',
 'sec2_6',
 'sec2_7',
 'sec3_0',
 'sec3_1',
 'sec3_2',
 'sec3_3',
 'sec3_4',
 'sec3_5',
 'sec3_6',
 'sec3_7',
 'formalaccount_b',
 'credit_b',
 'bankaccount_b',
 'loan_b',
 'secondaryedu_b',
 'advert_b',
 'retail_b',
 'manu_b',
 'serv_b',
 'food_b',
 'keeps_some_records_b',
 'marketing_b',
 'istough0_0',
 'istough5_0',
 'istough0_1',
 'istough5_1',
 'istough0_2',
 'istough5_2',
 'istough0_3',
 'istough5_3',
 'istough0_4',
 'istough5_4',
 'istough0_5',
 'istough5_5',
 'istough0_6',
 'istough5_6',
 'istough0_7',
 'istough5_7',
 'istough0_8',
 'istough5_8',
 'istough0_9',
 'istough5_9',
 'istough0_10',
 'istough5_10',
 'istough0_11',
 'istough5_11']

dfDandora = dfDandora[cols]

dfDandora = dfDandora.sort_values(['Lid'], ascending = [True])
any_new = dfDandora.filter(items = ['new_0',
 'new_1',
 'new_2',
 'new_3',
 'new_4',
 'new_5',
 'new_6',
 'new_7',
 'new_8',
 'new_9',
 'new_10',
 'new_11'])

any_drop = dfDandora.filter(items = ['dropped_0',
 'dropped_1',
 'dropped_2',
 'dropped_3',
 'dropped_4',
 'dropped_5',
 'dropped_6',
 'dropped_7',
 'dropped_8',
 'dropped_9',
 'dropped_10',
 'dropped_11'])

dfDandora['any_new'] = any_new.max(axis=1)
dfDandora['any_drop'] = any_drop.max(axis=1)
dfDandora['sum_drop'] = any_drop.sum(axis=1)
dfDandora['sum_new'] = any_drop.sum(axis=1)
dfDandora['share_new'] = dfDandora['sum_new']/dfDandora['probs5']
dfDandora['share_drop'] = dfDandora['sum_drop']/dfDandora['probs0']

dfOutput = dfDandora.copy()

#any_new " = 1 if mentions any issues at t=7 that aren't at t=1"
#any_drop " = 1 if does not mention an issue at t=7 is mentioned at t=1"
#share_new "Fraction of issues mentioned at t=7 that are not at t=1"
#share_drop "Fraction of issues not mentioned at t=7 that are at t=1"

'''Summarize for Control'''
dfControl = dfDandora.filter(items = ['any_new', 'any_drop', 'share_drop', 'share_new', 'treat'])
dfControl.loc[(dfControl['treat'] == 2)].describe()




'''
* ----------------------------------
* HOW DOES MENTOR ADVICE LINE UP WITH BASELINE DIFFICULTIES? (FIGURE 5A)
* ----------------------------------
'''
dfDandora = df_BDJDandora.copy()
dfDandora = dfDandora.set_index(['id', 'wave'])
dfDandora['wave'] = df_BDJDandora['wave'].values
dfDandora['id'] = df_BDJDandora['id'].values
dfDandora = dfDandora.rename(columns={"wave": "Lwave", "id": "Lid"})
dfDandora = dfDandora.loc[dfDandora['treat2'] == 4]

dfDandora = dfDandora.sort_values(['Lid','Lwave'], ascending = [True, True])
toughx = dfDandora['difficulties'].str.split(' ', expand = True)
toughx[0] = pd.to_numeric(toughx[0], errors='coerce')
toughx[1] = pd.to_numeric(toughx[1], errors='coerce')
toughx[2] = pd.to_numeric(toughx[2], errors='coerce')
toughx[3] = pd.to_numeric(toughx[3], errors='coerce')
toughx[4] = pd.to_numeric(toughx[4], errors='coerce')

toughx[4].value_counts()
toughx = toughx.rename(columns={0: "tough1", 1: "tough2", 2: "tough3", 3: "tough4", 4: "tough5"})
combined = pd.concat([dfDandora, toughx], axis=1)
dfDandora = combined.copy()
dfDandora = dfDandora.sort_values(['Lid','Lwave'], ascending = [True, True])

temp0 = dfDandora.copy()
for i in range(0, 12):
    temp0['_hold1'] = np.where((temp0.Lwave == 0), 0, np.nan)
    temp0['_hold1'] = np.where((((temp0.tough1 ==  i) & (temp0.Lwave == 0)) | 
            ((temp0.tough2 ==  i) & (temp0.Lwave == 0)) | ((temp0.tough3 ==  i) & (temp0.Lwave == 0)) | 
            ((temp0.tough4 ==  i) & (temp0.Lwave == 0)) | ((temp0.tough5 ==  i) & (temp0.Lwave == 0))), 1, np.nan)
    temp0['diff0_{}'.format(i)] = temp0.groupby(['Lid'], axis = 0)['_hold1'].transform('max')
    temp0 = temp0.drop(['_hold1'], axis = 1)
    
dfDandora = temp0.copy()

discusseverx = dfDandora['discussever'].str.split(' ', expand = True)

def toNum(df,x):
    df[x] = pd.to_numeric(df[x], errors = 'coerce')
    return df[x]

for i in range(0, 11):
    discusseverx[i] = toNum(discusseverx, i)
    
discusseverx = discusseverx.drop([0], axis = 1)


discusseverx = discusseverx.rename(columns={1: "discussever1", 2: "discussever2", 
                                            3: "discussever3", 4: "discussever4", 
                                            5: "discussever5", 6: "discussever6", 
                                            7: "discussever7", 8: "discussever8", 
                                            9: "discussever9",10:"discussever10"})
combined = pd.concat([dfDandora, discusseverx], axis=1)
dfDandora = combined.copy()

dfDandora = dfDandora.sort_values(['Lid'], ascending = [True])
temp1 = dfDandora.copy()

for i in range(0, 11):
    temp1['hold'] = 0
    temp1.loc[(temp1['discussever1'] == i) | 
            (temp1['discussever2'] == i) | 
            (temp1['discussever3'] == i) | 
            (temp1['discussever4'] == i) | 
            (temp1['discussever5'] == i) |
            (temp1['discussever6'] == i) |
            (temp1['discussever7'] == i) |
            (temp1['discussever8'] == i) |
            (temp1['discussever9'] == i) |
            (temp1['discussever10'] == i), 'hold'] = 1
   
    temp1['discussever_{}'.format(i)] = temp1.groupby(['Lid'], axis = 0)['hold'].transform('max')
    temp1 = temp1.drop(['hold'], axis = 1)

dfDandora = temp1.copy()

dfDandora = dfDandora[dfDandora["Lwave"] == 0]

keep = ['Lid', 'diff0_0', 'diff0_1', 'diff0_2', 'diff0_3', 'diff0_4', 'diff0_5', 'diff0_6', 'diff0_7', 'diff0_8', 'diff0_9', 'diff0_10', 'diff0_11', 'discussever_1', 'discussever_2','discussever_3','discussever_4','discussever_5','discussever_6','discussever_7','discussever_8','discussever_9','discussever_10']
dfDandora = dfDandora.filter(keep)



temp2 = dfDandora.copy()
for j in range(1, 11):
    temp2['mean_discussever_{}'.format(j)] = temp2['discussever_{}'.format(j)].mean()
    
    for i in range(0,12):
        temp2['hold'] = np.where((temp2['diff0_{}'.format(i)] == 1), temp2['discussever_{}'.format(j)], np.nan)
        temp2['mean_discussever_{}_if{}'.format(j, i)] = temp2['hold'].mean()
        temp2 = temp2.drop(['hold'], axis = 1)

dfDandora = temp2.copy()

dfOutput = dfDandora.copy()




temp5 = pd.DataFrame()    
for j in range (1,11):
    temp5 = temp5.append(pd.Series(), ignore_index=True)
    for i in range(0,12):
        temp5.at[j-1,'prob0_{}'.format(i)]= dfDandora['mean_discussever_{}_if{}'.format(j, i)].max()
    temp5.at[j-1, 'allprobs'] = dfDandora['mean_discussever_{}'.format(j)].values.max()
temp5['discussever'] = range(1,11)

newlab = ["Attract customers", "Product pricing", "Lower cost", "Product types", "Location" , "Where to buy" ,"Record keeping", "New investments", "Hours", "Take out loans"]
temp5["Discussed_Ever"] = newlab
temp5.to_csv(r'/Users/gopaljuneja/Desktop/Reproduced_MEK/Fig7.csv')
    
'''

* ----------------------------------
* HOW MANY TOPICS DO YOU DISCUSS WITH YOUR MENTOR? (FIGURE 5B)
* ----------------------------------
'''
dfDandora = df_BDJDandora.copy()

cond1 = dfDandora["treat2"] == 4   
cond2 = dfDandora["wave"] <= 6
dfDandora = dfDandora[cond1 & cond2]
    

dfDandora.loc[(dfDandora.meet2 == 1), "wavem"] = dfDandora.wave
dfDandora['max_wave'] = dfDandora.groupby(['id'], axis = 0)['wavem'].transform('max')
dfDandora = dfDandora.drop(['wavem'], axis = 1)



dx = dfDandora['discuss'].str.split(' ', expand = True)
dx[0] = pd.to_numeric(dx[0], errors='coerce')
dx[1] = pd.to_numeric(dx[1], errors='coerce')
dx[2] = pd.to_numeric(dx[2], errors='coerce')
dx[3] = pd.to_numeric(dx[3], errors='coerce')
dx[4] = pd.to_numeric(dx[4], errors='coerce')
dx[5] = pd.to_numeric(dx[5], errors='coerce')
dx[6] = pd.to_numeric(dx[6], errors='coerce')
dx[7] = pd.to_numeric(dx[7], errors='coerce')
dx[8] = pd.to_numeric(dx[8], errors='coerce')
dx[9] = pd.to_numeric(dx[9], errors='coerce')
dx[10] = pd.to_numeric(dx[10], errors='coerce')
dx = dx.rename(columns={0: "d1", 1: "d2", 2: "d3", 3: "d4", 4: "d5", 5: "d6", 6: "d7", 7: "d8", 8: "d9", 9: "d10", 10: "d11" })
combined = pd.concat([dfDandora, dx], axis=1)
dfDandora = combined.copy()
dfDandora = dfDandora.sort_values(['id'], ascending = [True])

temp5 = dfDandora.copy()

for j in range(1,11):
    temp5['h'] = 0
    for i in range(1,12):
        #print (temp5[temp5['d{}'.format(i)].values == j])
        temp5['h'] = np.where((temp5['d{}'.format(i)].values == j), 1, temp5['h'])
        
        #temp5['h'] = np.where(temp5['d{}'.format(i)].values == j, 1, 0) 
        #temp5.loc[(temp5['d{}'.format(i)].values == j), 'h'] = 1
        
    temp5['t_{}'.format(j)] = temp5.groupby(['id'], axis = 0)['h'].transform('max')
    temp5 = temp5.drop(['h'], axis = 1)




temp5.loc[temp5['d{}'.format(i)] == j,'h'] =1
list(temp5.id.unique().astype(str))
temp5.id.value_counts()

fig5b = pd.DataFrame(data)
fig5b = fig5b.astype(float)
fig5c["Attract customers" , "Product pricing", "Lower cost" ,"Product types" ,"Location",  "Where to buy" ,"Record keeping" , "New investments" ,"Hours",  "Take out loans"] = ["Attract customers" , "Product pricing", "Lower cost" ,"Product types" ,"Location",  "Where to buy" ,"Record keeping" , "New investments" ,"Hours",  "Take out loans"]

discuss
12345678910
mean_twice0 .6951219
.1428571
.1578947
.1538462
.2
.1
.4313726
.1578947
0
0
mean_twice1 =
.7086614
.1590909
.1923077
.1578947
.1388889
.1707317
.4246575
.1538461
.09375
0


data = {'id':['Tom', 'nick', 'krish', 'jack'], 'Age':[20, 21, 19, 18]}

fig5c = pd.DataFrame({'discuss': [1,2,3,4,5,6,7,8,9,10],'mean_twice0':[.6951219,
.1428571,
.1578947,
.1538462,
.2,
.1,
.4313726,
.1578947,
0,
0], 'mean_twice1': [.7086614,
.1590909,
.1923077,
.1578947,
.1388889,
.1707317,
.4246575,
.1538461,
.09375,
0]})
                    
fig5c.to_csv(r'/Users/gopaljuneja/Desktop/Reproduced_MEK/Fig5c.csv')

fig5b.to_csv(r'/Users/gopaljuneja/Desktop/Reproduced_MEK/Fig5b.csv')


'''----------------------------*'''
dfDandora = df_BDJDandora.copy()

dfDandora = dfDandora.loc[dfDandora['treat2'] == 4]

dfDandora = dfDandora.sort_values(['id','wave'], ascending = [True, True])


dfDandora = dfDandora[(dfDandora.wave.values != 0) & (dfDandora.wave.values != 7)]

dfDandora = dfDandora[dfDandora.meet2.values == 1]
dfDandora = dfDandora.drop(['meet2'], axis = 1)

dx = dfDandora['discuss'].str.split(' ', expand = True)
dx[0] = pd.to_numeric(dx[0], errors='coerce')
dx[1] = pd.to_numeric(dx[1], errors='coerce')
dx[2] = pd.to_numeric(dx[2], errors='coerce')
dx[3] = pd.to_numeric(dx[3], errors='coerce')
dx[4] = pd.to_numeric(dx[4], errors='coerce')
dx[5] = pd.to_numeric(dx[5], errors='coerce')
dx[6] = pd.to_numeric(dx[6], errors='coerce')
dx[7] = pd.to_numeric(dx[7], errors='coerce')
dx[8] = pd.to_numeric(dx[8], errors='coerce')
dx[9] = pd.to_numeric(dx[9], errors='coerce')
dx[10] = pd.to_numeric(dx[10], errors='coerce')
dx = dx.rename(columns={0: "d1", 1: "d2", 2: "d3", 3: "d4", 4: "d5", 5: "d6", 6: "d7", 7: "d8", 8: "d9", 9: "d10", 10: "d11" })
combined = pd.concat([dfDandora, dx], axis=1)
dfDandora = combined.copy()


temp6 = dfDandora.copy()

for i in range(0, 11):
    temp6['discuss_{}'.format(i)] = 0
    temp6.loc[(temp6['d1'] == i) | 
            (temp6['d2'] == i) | 
            (temp6['d3'] == i) | 
            (temp6['d4'] == i) | 
            (temp6['d5'] == i) |
            (temp6['d6'] == i) |
            (temp6['d7'] == i) |
            (temp6['d8'] == i) |
            (temp6['d9'] == i) |
            (temp6['d10'] == i) |
            (temp6['d11'] == i), 'discuss_{}'.format(i)] = 1

dfDandora = temp6.copy()

dfDandora = dfDandora.drop(['d1','d2','d3','d4','d5','d6','d7','d8','d9','d10','d11','discuss'], axis = 1)

dfDandora['diff'] = dfDandora.groupby('id')['wave'].apply(lambda x: x.shift(-1) - x)
dfDandora['diff'].value_counts()

temp7 = dfDandora.copy()
temp7['diff'] = temp7['diff'].astype(float)
for i in range(0, 11):
    cond = ((temp7['discuss_{}'.format(i)].shift() == 1) & (temp7['diff'] == 1))
    temp7.loc[temp7[cond].groupby('id'), 'twice0_{}'.format(i)] = 0
