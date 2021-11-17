'''
Created on Jan 6, 2021

@author: leon
'''
import pandas as pd

def get_ticker_list(path):
    df=pd.read_csv(path)
    ticker_list = list(df['Symbol'])
    return ticker_list
