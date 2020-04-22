# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 14:49:50 2020

@author: Apurva
"""


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------- MAIN METHOD --------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------


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



# -----------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------- END METHOD --------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

