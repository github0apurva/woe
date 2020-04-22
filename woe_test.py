# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 17:24:30 2020

@author: Apurva
"""

import numpy as np
import pandas as pd
import wget
import woe_chi as wc


# ---------------------------------------------------------- Load Data -------------------------------------------------------------
data_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/credit-screening/crx.data"
wget.download(data_url,'crx.csv')
# ---------------------------------------------------------- Data Ready ------------------------------------------------------------
crx_base = pd.read_csv("crx.csv", names = ["A1","A2","A3","A4","A5","A6","A7","A8","A9","A10","A11","A12","A13","A14","A15","A16"] )
crx_base.replace('?', np.NaN, inplace = True)
crx_base['A161']= np.where(crx_base['A16'] == '+' , 1, 0)
# -------------------------------------------------- Tweeks for further usage ------------------------------------------------------
crx_base['A81'] = crx_base['A8'].clip( 0,7)
crx_base['A111'] = crx_base['A11'].clip( 0,19)
crx_base['A112'] = crx_base['A11'].clip( 0,15) + 10
crx_base['A2'] = crx_base['A2'].astype('float')




# ------------------------------------------------ Calling the cal_woe method ------------------------------------------------------
# The method can handle both continuous and discrete variables. It creates a seperate bucket for missing values.
var_param , var_bin_woe = wc.cal_woe (x=crx_base['A2'], y=crx_base['A161'], typex = 'cont', binx = 10  )
# The default bin is 10, you can change as required. If it is more than unique value of continous variable, it will change to latter.
var_param , var_bin_woe = wc.cal_woe (x=crx_base['A111'], y=crx_base['A161'], typex = 'cont', binx = 20  )
# If bin is specificed for a discrete variable, it will autocorrect to number of unique instances. 
var_param , var_bin_woe = wc.cal_woe (x=crx_base['A1'], y=crx_base['A161'], typex = 'disc' , binx = 20 )


# ------------------------------------------------ Calling the cal_woe method for multivariables -----------------------------------
# for handling multiple variables in one go, mention the type and bin as list for all the passed variables.
var_param , var_bin_woe = wc.cal_woe (x=crx_base[['A7','A1','A112']], y=crx_base['A161'], typex = ['disc','disc','cont'] , binx = [10,10,20] )
# The output will be a dataframe for IV & Chi Square values
# And a dictionary for bin-wise WOE. The key of this will be the variable name ofcourse.

