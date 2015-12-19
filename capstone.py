#resource http://www.datarobot.com/blog/multiple-regression-using-statsmodels/

import numpy as np 
import pandas as pd
import os
import sqlite3
import csv
import glob
import statsmodels.api as sm
from patsy import dmatrices

#final_regression_V2.csv

# dbet = datasets.load_diabetes()
# print dbet


# a = [5, 6, 7, 8, 9, 0, 12, 4, 6, 8]
# 
# #print a[-1] #8
# #print a[2]	#7
# #print a[:-1] #[5, 6, 7, 8, 9, 0, 12, 4, 6]
# print a[:-4] #8

'Daily_Tweet_Total'
# 'Agg_Sentiment'
# 'Avg_Sentiment'
# 'Agg_User_Sentiment'
# 'Avg_User_Sentiment'
# 'Agg_RT'

############## Building the DataFrame ############## 
path =r'/ # use your path
df = pd.read_csv(path+'/final_regression_V2.csv', header=0)

############# The Regression ################



y, X = dmatrices('LogClose ~  LogAvg_Sent + LogAgg_RT ', data=df, return_type='dataframe')
#y, X = dmatrices('Close ~  Avg_Sentiment + Agg_RT', data=df, return_type='dataframe') #Ribge Regression on this

#print df.head()

reg= sm.GLS(y,X).fit()

print reg.summary()
# print reg.mse_model()
# print reg.mse_resid()
# print reg.mse_total()
################# Model 6#################

#y, X = dmatrices('Daily_Change ~  Avg_Sentiment + Agg_RT', data=df, return_type='dataframe')

# Warnings:
# [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
# Jonathans-MacBook-Pro:work jcreem$ python capstone.py
#                             OLS Regression Results                            
# ==============================================================================
# Dep. Variable:           Daily_Change   R-squared:                       0.137
# Model:                            OLS   Adj. R-squared:                  0.084
# Method:                 Least Squares   F-statistic:                     2.610
# Date:                Thu, 17 Dec 2015   Prob (F-statistic):             0.0886
# Time:                        23:07:45   Log-Likelihood:                -38.246
# No. Observations:                  36   AIC:                             82.49
# Df Residuals:                      33   BIC:                             87.24
# Df Model:                           2                                         
# Covariance Type:            nonrobust                                         
# =================================================================================
#                     coef    std err          t      P>|t|      [95.0% Conf. Int.]
# ---------------------------------------------------------------------------------
# Intercept        -0.2835      0.290     -0.976      0.336        -0.874     0.307
# Avg_Sentiment     1.0959      0.610      1.797      0.082        -0.145     2.337
# Agg_RT           -0.0004      0.000     -1.874      0.070        -0.001  3.55e-05
# ==============================================================================
# Omnibus:                        1.147   Durbin-Watson:                   2.001
# Prob(Omnibus):                  0.564   Jarque-Bera (JB):                0.968
# Skew:                           0.159   Prob(JB):                        0.616
# Kurtosis:                       2.262   Cond. No.                     3.88e+03
# ==============================================================================

##################Model 5##################

#y, X = dmatrices('Close ~  L1Close + Avg_Sentiment + Agg_RT', data=df, return_type='dataframe')

 #                            GLS Regression Results                            
# ==============================================================================
# Dep. Variable:                  Close   R-squared:                       1.000
# Model:                            GLS   Adj. R-squared:                  1.000
# Method:                 Least Squares   F-statistic:                 4.397e+04
# Date:                Thu, 17 Dec 2015   Prob (F-statistic):           6.61e-58
# Time:                        21:18:30   Log-Likelihood:                -37.199
# No. Observations:                  36   AIC:                             82.40
# Df Residuals:                      32   BIC:                             88.73
# Df Model:                           3                                         
# Covariance Type:            nonrobust                                         
# =================================================================================
#                     coef    std err          t      P>|t|      [95.0% Conf. Int.]
# ---------------------------------------------------------------------------------
# Intercept        -0.3359      0.289     -1.163      0.254        -0.924     0.253
# L1Close           0.9940      0.004    227.614      0.000         0.985     1.003
# Avg_Sentiment     1.9291      0.851      2.266      0.030         0.195     3.663
# Agg_RT           -0.0003      0.000     -1.255      0.219        -0.001     0.000
# ==============================================================================
# Omnibus:                        1.035   Durbin-Watson:                   2.062
# Prob(Omnibus):                  0.596   Jarque-Bera (JB):                1.050
# Skew:                           0.303   Prob(JB):                        0.592
# Kurtosis:                       2.424   Cond. No.                     5.23e+03

##################Model 4###################
#y, X = dmatrices('Close ~  Agg_Sentiment + Avg_Sentiment + Agg_RT', data=df, return_type='dataframe')
 #                            GLS Regression Results                            
# ==============================================================================
# Dep. Variable:                  Close   R-squared:                       0.646
# Model:                            GLS   Adj. R-squared:                  0.612
# Method:                 Least Squares   F-statistic:                     19.43
# Date:                Thu, 17 Dec 2015   Prob (F-statistic):           2.34e-07
# Time:                        21:16:41   Log-Likelihood:                -168.37
# No. Observations:                  36   AIC:                             344.7
# Df Residuals:                      32   BIC:                             351.1
# Df Model:                           3                                         
# Covariance Type:            nonrobust                                         
# =================================================================================
#                     coef    std err          t      P>|t|      [95.0% Conf. Int.]
# ---------------------------------------------------------------------------------
# Intercept         2.9143     12.667      0.230      0.820       -22.888    28.717
# Agg_Sentiment     0.0229      0.012      1.864      0.072        -0.002     0.048
# Avg_Sentiment   110.1308     27.726      3.972      0.000        53.655   166.606
# Agg_RT           -0.0273      0.026     -1.033      0.309        -0.081     0.027
# ==============================================================================
# Omnibus:                        0.923   Durbin-Watson:                   1.484
# Prob(Omnibus):                  0.630   Jarque-Bera (JB):                0.967
# Skew:                           0.293   Prob(JB):                        0.617
# Kurtosis:                       2.451   Cond. No.                     1.15e+04
# ==============================================================================

#############Model 3###################

#y, X = dmatrices('Close ~ L1Close + Daily_Tweet_Total + Agg_Sentiment + Avg_Sentiment + Agg_RT', data=df, return_type='dataframe')

                            #GLS Regression Results                            
# ==============================================================================
# Dep. Variable:                  Close   R-squared:                       1.000
# Model:                            GLS   Adj. R-squared:                  1.000
# Method:                 Least Squares   F-statistic:                 2.570e+04
# Date:                Thu, 17 Dec 2015   Prob (F-statistic):           1.64e-53
# Time:                        21:13:42   Log-Likelihood:                -36.512
# No. Observations:                  36   AIC:                             85.02
# Df Residuals:                      30   BIC:                             94.52
# Df Model:                           5                                         
# Covariance Type:            nonrobust                                         
# =====================================================================================
#                         coef    std err          t      P>|t|      [95.0% Conf. Int.]
# -------------------------------------------------------------------------------------
# Intercept            -0.5986      0.384     -1.558      0.130        -1.384     0.186
# L1Close               0.9963      0.005    202.121      0.000         0.986     1.006
# Daily_Tweet_Total     0.0002      0.000      0.634      0.531        -0.000     0.001
# Agg_Sentiment        -0.0005      0.000     -1.080      0.289        -0.001     0.000
# Avg_Sentiment         2.1942      0.898      2.443      0.021         0.360     4.029
# Agg_RT             4.616e-06      0.001      0.005      0.996        -0.002     0.002
# ==============================================================================
# Omnibus:                        1.822   Durbin-Watson:                   2.011
# Prob(Omnibus):                  0.402   Jarque-Bera (JB):                1.334
# Skew:                           0.245   Prob(JB):                        0.513
# Kurtosis:                       2.195   Cond. No.                     2.50e+04
# ==============================================================================


############# Model 2 ##################
#y, X = dmatrices('Close ~ L1Close + Open + High + Low + Daily_Tweet_Total + Agg_Sentiment + Avg_Sentiment + Agg_RT', data=df, return_type='dataframe')

#                             GLS Regression Results                            
# ==============================================================================
# Dep. Variable:                  Close   R-squared:                       1.000
# Model:                            GLS   Adj. R-squared:                  1.000
# Method:                 Least Squares   F-statistic:                 2.431e+05
# Date:                Thu, 17 Dec 2015   Prob (F-statistic):           1.64e-63
# Time:                        21:11:33   Log-Likelihood:                 14.290
# No. Observations:                  36   AIC:                            -10.58
# Df Residuals:                      27   BIC:                             3.673
# Df Model:                           8                                         
# Covariance Type:            nonrobust                                         
# =====================================================================================
#                         coef    std err          t      P>|t|      [95.0% Conf. Int.]
# -------------------------------------------------------------------------------------
# Intercept             0.0003      0.120      0.002      0.998        -0.246     0.247
# L1Close              -0.1864      0.087     -2.147      0.041        -0.365    -0.008
# Open                 -0.6592      0.097     -6.771      0.000        -0.859    -0.459
# High                  1.0704      0.124      8.600      0.000         0.815     1.326
# Low                   0.7730      0.125      6.203      0.000         0.517     1.029
# Daily_Tweet_Total -8.978e-05   7.57e-05     -1.186      0.246        -0.000  6.55e-05
# Agg_Sentiment      3.701e-06      0.000      0.031      0.975        -0.000     0.000
# Avg_Sentiment        -0.0792      0.259     -0.306      0.762        -0.610     0.451
# Agg_RT                0.0004      0.000      1.715      0.098     -7.94e-05     0.001
# ==============================================================================
# Omnibus:                        2.370   Durbin-Watson:                   2.349
# Prob(Omnibus):                  0.306   Jarque-Bera (JB):                1.857
# Skew:                           0.399   Prob(JB):                        0.395
# Kurtosis:                       2.224   Cond. No.                     2.87e+04
# ==============================================================================

#######################Model 1####################
#                             GLS Regression Results                            
# ==============================================================================
# Dep. Variable:                  Close   R-squared:                       1.000
# Model:                            GLS   Adj. R-squared:                  1.000
# Method:                 Least Squares   F-statistic:                 1.146e+05
# Date:                Thu, 17 Dec 2015   Prob (F-statistic):           1.45e-61
# Time:                        21:21:26   Log-Likelihood:                -40.825
# No. Observations:                  36   AIC:                             85.65
# Df Residuals:                      34   BIC:                             88.82
# Df Model:                           1                                         
# Covariance Type:            nonrobust                                         
# ==============================================================================
#                  coef    std err          t      P>|t|      [95.0% Conf. Int.]
# ------------------------------------------------------------------------------
# Intercept      0.0981      0.224      0.438      0.664        -0.357     0.553
# L1Close        0.9990      0.003    338.501      0.000         0.993     1.005
# ==============================================================================
# Omnibus:                        1.353   Durbin-Watson:                   2.021
# Prob(Omnibus):                  0.508   Jarque-Bera (JB):                1.317
# Skew:                           0.399   Prob(JB):                        0.518
# Kurtosis:                       2.510   Cond. No.                         132.
# ==============================================================================



# 'Date'
# 'Symbol'
# 'Open'
# 'High'
# 'Low'
# 'Close'
# 'Daily Change'
# 'L1Close'
# 'L2Close'
# 'L3Close'
# 'L4Close'
# 'L5Close'
# 'Volume'
# 'L1Volume'
# 'L2Volume'
# 'L3Volume'
# 'L4Volume'
# 'L5Volume'
# 'L1Open'
# 'L2Open'
# 'L3Open'
# 'L4Open'
# 'L5Open'
# 'L1High'
# 'L2High'
# 'L3High'
# 'L4High'
# 'L5High'
# 'L1Low'
# 'L2Low'
# 'L3Low'
# 'L4Low'
# 'L5Low'
# 'Daily_Tweet_Total'
# 'Agg_Sentiment'
# 'Avg_Sentiment'
# 'Agg_User_Sentiment'
# 'Avg_User_Sentiment'
# 'Agg_RT'
