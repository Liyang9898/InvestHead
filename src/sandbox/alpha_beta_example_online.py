
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from sklearn.linear_model import LinearRegression
import numpy as np


from pandas_datareader import data as pdr
import yfinance as yf

import statsmodels.api as sm
from statsmodels import regression

def cov(l1,l2):
    array1 = np.array(l1)
    array2 = np.array(l2)
    return np.cov(array1, array2)

target_ticker = "MSFT"
baseline_ticker = "SPY"
start_date = "2016-07-31"
end_date = "2021-07-31"


def linreg(x,y):
    x = sm.add_constant(x)
    model = regression.linear_model.OLS(y,x).fit()
    # We are removing the constant
    x = x[:, 1]
    return model.params[0], model.params[1]


def alpha_beta():
    # https://blog.quantinsti.com/asset-beta-market-beta-python/
    yf.pdr_override()
    
    df1 = pdr.get_data_yahoo(target_ticker, start=start_date, end=end_date)
    df2 = pdr.get_data_yahoo(baseline_ticker, start=start_date, end=end_date)
    
    # We have to take the percent changes to get to returns hence we will use .pct_change()
    # We do not want the first (0th) element because it is NAN
    return_target = df1.Close.pct_change()[1:]
    return_baseline = df2.Close.pct_change()[1:]
    
    # We will plot the returns of Google and S&P500 against each other
#     plt.figure(figsize=(20,10))
#     return_target.plot()
#     return_baseline.plot()
#     plt.ylabel(f"Daily Return of {target_ticker} and {baseline_ticker}")
#     plt.show()
    
    X = return_baseline.values
    Y = return_target.values

    alpha, beta = linreg(X,Y)
    print('alpha: ' + str(alpha))
    print('beta: ' + str(beta))
    
    cov_matrix = cov(X,Y)
    covariance = cov_matrix[0][1]
    variance  = np.var(X)
    beta_2 = covariance / variance

    print(beta_2)

    
#     X2 = np.linspace(X.min(), X.max(), 100)
#     Y_hat = X2 * beta + alpha
#     
#     
#     plt.figure(figsize=(10,7))
#     plt.scatter(X, Y, alpha=0.3) # Plot the raw data
#     plt.xlabel(f"{baseline_ticker} Daily Return")
#     plt.ylabel(f"{target_ticker} Daily Return")
#     plt.plot(X2, Y_hat, 'r', alpha=0.9)
#     
#     plt.show()
    
    
alpha_beta()

