# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 14:49:50 2020

@author: Apurva
"""

import numpy as np
import pandas as pd
import wget


data_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/credit-screening/crx.data"
wget.download(data_url,'crx.csv')
crx_base = pd.read_csv("crx.csv", names = ["A1","A2","A3","A4","A5","A6","A7","A8","A9","A10","A11","A12","A13","A14","A15","A16"] )
crx_base.replace('?', np.NaN, inplace = True)
crx_base['A161']= np.where(crx_base['A16'] == '+' , 1, 0)
crx_base['A81'] = crx_base['A8'].clip( 0,7)
crx_base['A111'] = crx_base['A11'].clip( 0,19)
crx_base['A112'] = crx_base['A11'].clip( 0,15) + 10
crx_base['A2'] = crx_base['A2'].astype('float')


def cal_woe(x, y, typex = 'cont' , binx = 10 ):
    from scipy.stats import chi2_contingency
    # ------------------------------------------------------------ checking y variable ------------------------------------------------------------------------
    if y.isnull().sum() > 0:
        print ("check y variable, contains missing = " , y.isnull().sum() )
        return np.nan , np.nan ,np.nan

    if y.nunique() != 2:
        print ("check y variable, classes more than 2" )
        return np.nan , np.nan ,np.nan


    # ------------------------------------------------------------ actual function   --------------------------------------------------------------------------
    def cal_back (x1 , y1, typex1 , binx1 ):
        # different function for discrete and continuous variables
        if typex1 == 'cont' and binx1 < x1.nunique() :
            xmin = x1.min()
            rng = ( x1.max() - xmin ) / binx1
            a = ( np.round(( ( x1 - x1.min() ) / rng ),0 )).clip(0 , binx1-1 ).astype('O')
            x1 = a
            bin_range = x1.unique()
        # checking if the discrete variable ( convereted discrete for cont) is object dtype or not
        if x1.dtype != 'O':
            x1 = x1.astype('O')
        # adding one more bin for missing data
        x1 = x1.fillna('woe_mis')
        # counting number of bins for discrete variables
        binx1 = x1.nunique()
        # calculation of woe and iv
        a = pd.crosstab( x1, y1, normalize = 'columns' ,margins=True)
        b = pd.crosstab( x1, y1, margins=True)
        b['woe'] = np.log(a[1]/a[0])
        b['iv'] = (a[1]-a[0]) * b['woe']
        if typex1 == 'cont' :
            b.rename(index={'All':np.inf, 'woe_mis':-1.111},inplace=True)
            b.sort_index(inplace = True)
            b.rename(index={np.inf:'All', -1.111:'woe_mis'},inplace=True)
        else :
            b.sort_values(by = 'woe' , inplace = True)
        b[['woe','iv']] = b[['woe','iv']].replace([np.inf, -np.inf], np.nan )
        c = b['iv'].sum(skipna = True)
        b['iv'] = b['iv'].where( b.index != 'All' , c )
        # calculating chi square value
        stat, p, dof, expected = chi2_contingency(np.array(pd.crosstab ( y1, x1)))
        d = []
        d.append(binx1)
        d.append(c)
        d.append("{:.4f}".format(p))
        d.append(dof)
        d.append(stat)
        c = pd.DataFrame( d, index = ['bins','iv','chi2-p','chi2-dof','chi2-value' ]  ).T
        try:
            b['low_bin_value'] = [ np.nan if (type(x) == str) else ( xmin + x*rng ) for x in b.index  ]
        except:
            pass
        return  c , b


    # ------------------------------------------------------------ for more than 1 x --------------------------------------------------------------------------
    shp = len(x.shape)
    if shp > 1:
        xs2 = x.shape[1]
        try:
            if len(typex) != xs2 or len(binx) != xs2 :
                print ( 'input for typex or bin is wrong')
                return np.nan , np.nan ,np.nan
        except:
            print ( 'input for bin is wrong')
            return np.nan , np.nan ,np.nan
        bo = {}
        for i in range(xs2):
            nm = x.columns[i]
            ac, ab, = cal_back  (x1=x[nm], y1=y, typex1 = typex[i] , binx1 = binx[i]  )
            if i == 0:
                co  = ac.rename(index={0:nm})
            else:
                co = pd.concat([co,ac.rename(index={0:nm})], axis = 0)
            bo[nm] = ab
        print ('Done')

    # ------------------------------------------------------------ for just 1 x      --------------------------------------------------------------------------
    else:
        co, bo = cal_back (x1=x, y1=y, typex1 = typex , binx1 = binx  )


    # ------------------------------------------------------------ return valid output ------------------------------------------------------------------------
    return co, bo




var_param , var_bin_woe = cal_woe (x=crx_base['A2'], y=crx_base['A161'], typex = 'cont', binx = 10  )
var_param , var_bin_woe = cal_woe (x=crx_base['A111'], y=crx_base['A161'], typex = 'cont', binx = 20  )
var_param , var_bin_woe = cal_woe (x=crx_base['A1'], y=crx_base['A161'], typex = 'disc' , binx = 20 )
var_param , var_bin_woe = cal_woe (x=crx_base[['A7','A1','A112']], y=crx_base['A161'], typex = ['disc','disc','cont'] , binx = [10,10,20] )

var_bin_woe['A112']

crx_base.info()
crx_base.head()
crx_base['A161'].value_counts()
crx_base.describe()
crx_base[['A7','A1','A112']].shape[1]

x1 = crx_base['A7']
rng = ( x1.max() - x1.min() ) / binx1
a = ( np.round(( ( x1 - x1.min() ) / rng ),0 )).clip(0 , binx1-1 ).astype('O')
x1 = a
bin_range = x1.unique()

1. handle y missing Done
2. include bin min through index Done
3. chi square


x1 = crx_base['A1']
y1 = crx_base['A161']
from scipy.stats import chi2_contingency
stat, p, dof, expected = chi2_contingency(np.array(pd.crosstab ( y1, x1)))
print ( "{:.4f}".format(p) )



d = []
d.append(c)
d.append(bin_count)
d.append("{:.4f}".format(p))
d.append(dof)
d.append(stat)



