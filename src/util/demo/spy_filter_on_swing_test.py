from util.util_pandas import gen_csv_from_list_of_val
from util.util_time import gen_date_list_in_range
import pandas as pd

res = gen_date_list_in_range('2022-01-01', '2022-01-05', True)
gen_csv_from_list_of_val(res, 'date', 'D:/f_data/temp/spy_filter.csv')
# print(res)

df = pd.read_csv('D:/f_data/temp/spy_filter.csv')
# print(df)


def gen_position_opened_date_from_trades(trade_csv, open_date_csv):
    df_trade = pd.read_csv(trade_csv)
    open_dates = []
    for i in range(0, len(df_trade)):
        s = df_trade.loc[i, 'entry_ts'].split(' ')[0]
        e = df_trade.loc[i, 'exit_ts'].split(' ')[0]
        open_dates_trade = gen_date_list_in_range(s, e, False)
        open_dates = open_dates + open_dates_trade
    
    gen_csv_from_list_of_val(open_dates, 'date', 'D:/f_data/temp/spy_filter4.csv')
        

trade_csv = 'D:/f_data/analysis/20220303_spy_alone/consec.csv'
open_date_csv = 'D:/f_data/temp/spy_filter2.csv'
gen_position_opened_date_from_trades(trade_csv, open_date_csv)