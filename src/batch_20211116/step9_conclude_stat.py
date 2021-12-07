from datetime import datetime

from api.api import api_download_ticker
from batch_20211116.batch_20211116_lib.constant import PORTFOLIO_TIME_SERIES_FOLDER_RUSSLL1000
import pandas as pd
from util.general_ui import plot_bars_from_xy_list, plot_points_from_xy_list


def get_benchmark():
    start = '2009-01-01'
    end = '2022-01-01'
    interval = '1d'
    ticker = 'SPY'
    cnt = 0
    
    path = 'D:/f_data/temp/spy20211207.csv'
    
    api_download_ticker(ticker, start, end, path, interval)
    df = pd.read_csv(path)
    
    df['date']=df.apply(lambda row : str(datetime.fromtimestamp(int(row['unixtime'])).strftime('%Y-%m-%d')), axis = 1)
    df['spy'] = df['Close']
    base = df.loc[0,'spy']
    df['spy'] = df['spy'] / base
    df=df[['date','spy']]
    df=df.copy()
    return df

df_benchmark = get_benchmark()
result_position_path = PORTFOLIO_TIME_SERIES_FOLDER_RUSSLL1000 + 'position.csv'
df_result_position = pd.read_csv(result_position_path)
m_result = pd.merge(df_result_position, df_benchmark, how="inner", on="date")
x_list = m_result['date'].to_list()
y_list = {'roll':m_result['roll'].to_list(),'spy':m_result['spy'].to_list()}
# print(x_list)
plot_points_from_xy_list(x_list, y_list)
print(m_result)


# todo
# compare with spy 
# alpha, beta, align 
# win rate, win_lose_pnl_ratio, 
# -------------
# 4% not take profit, upper ma gap select