"""
this file plot stock chart during recession to check failure reason
"""
from api.api import api_download_ticker, api_gen_indicator
import pandas as pd
from util.general_ui import plot_candle_stick
from util.util_time import date_add_days


def plot(date, ticker):
    """
    plot ticker 2 year before and after, mark date
    """
    df = download_st_df(ticker=ticker, date=date, front_offset=180, back_offset=180)    
    plot_candle_stick(df, date_marker=[date], date_marker2=[date], ticker=ticker, path=None)


def download_st_df(ticker, date, front_offset, back_offset):
    """
    """
    s = date_add_days(date, -front_offset)
    e = date_add_days(date, back_offset)
    st_csv = 'D:/f_data/temp/pic_temp/xxx.csv'
    idc_csv = 'D:/f_data/temp/pic_temp/xxx2.csv'
    api_download_ticker(ticker, s, e, st_csv, interval='1d', norgate=True)
    api_gen_indicator(st_csv, idc_csv, s, e)
    df = pd.read_csv(idc_csv)
    return df


path = 'D:/f_data/batch_20220214/DEBUG/intermediate_per_track_trades_2001_negative_csv_simple.csv'
df = pd.read_csv(path)
df['date'] = pd.to_datetime(df['entry_ts'])
s_idx = 75
offset = 5

for i in range(0,len(df)):
    if i >= s_idx and i < s_idx + offset:
        date = str(df.loc[i, 'date']).split(' ')[0]
        ticker = df.loc[i, 'ticker']
        plot(date, ticker)
