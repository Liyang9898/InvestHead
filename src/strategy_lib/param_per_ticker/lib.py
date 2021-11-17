import pandas as pd
from version_master.version import ema21_ma50_gap_threshold


def get_strategy_param_per_ticker(ticker):
    param = pd.read_csv(ema21_ma50_gap_threshold)
    ticker_list=param['ticker'].to_list()
    if ticker not in ticker_list:
        return None
    ticker_param = param[param['ticker']==ticker]
    ticker_param_dic = list(ticker_param.T.to_dict().values())[0]
    
    return ticker_param_dic


def get_param_ema21_ma50_gap(ticker):
    param = get_strategy_param_per_ticker(ticker)
    if param is None:
        return None
    return param['model']
  
# res = get_param_ema21_ma50_gap(ticker='AMD')
# print(res)

