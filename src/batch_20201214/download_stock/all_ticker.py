import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from plotly.graph_objs import layout

import numpy as np
import plotly.express as px


def get_all_ticker_info():
    path_in = """D:/f_data/all_ticker/companylist.csv"""
    path = path_in
    df = pd.read_csv(
        path,
        sep=',',
        header=0,
        names=['ticker', 'name','last_sale','market_cap','ipo_year','sector','industry','summary_quote','na']
    )
    dic = df.to_dict(orient='records')
    
    res = {}
    for ticker in dic:
        res[ticker['ticker']] = ticker
    return res

def get_all_ticker_list():
    res= get_all_ticker_info()
    return list(res.keys())

# res= get_all_ticker_info()
# print(res)
# list_tickers = get_all_ticker_list()
# print(list_tickers)



def create_list_of_filepaths():
    list_tickers = get_all_ticker_list()
    list_tickers.remove('ZTEST')
    list_tickers.remove('CIICW')
    list_tickers.remove('HAIN')
    list_tickers.remove('ZNWAA')

    return list_tickers
        
        
# paths = create_list_of_filepaths()
# print(paths)