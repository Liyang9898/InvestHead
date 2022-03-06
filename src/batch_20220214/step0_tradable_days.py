from batch_20220214.batch_20220214_lib.constant import START_DATE, END_DATE, PATH_TRADABLE_DAYS, \
    path_spx_open_position_csv, use_trade_position_open_days
import pandas as pd
from util.util_pandas import gen_csv_from_list_of_val
from util.util_time import gen_date_list_in_range


"""
This section output a csv to 'PATH_TRADABLE_DAYS'
We only open position when the day exist in 'PATH_TRADABLE_DAYS'
"""


def gen_position_opened_date_from_trades(trade_csv, open_date_csv):
    df_trade = pd.read_csv(trade_csv)
    open_dates = []
    for i in range(0, len(df_trade)):
        s = df_trade.loc[i, 'entry_ts'].split(' ')[0]
        e = df_trade.loc[i, 'exit_ts'].split(' ')[0]
        open_dates_trade = gen_date_list_in_range(s, e, False)
        open_dates = open_dates + open_dates_trade
    
    gen_csv_from_list_of_val(open_dates, 'date', open_date_csv)
    

def gen_tradable_days(start_date, end_date, trade_file, path_tradable_days, use_trade_position_open_days=False):
    if not use_trade_position_open_days:
        """
        option 1: (CAN ONLY PICK ONE OPTION !!!!!)
        all days are tradable
        """
        res = gen_date_list_in_range(start_date, end_date, True)
        gen_csv_from_list_of_val(res, 'date', path_tradable_days)
    
    else:
        """
        option 2: (CAN ONLY PICK ONE OPTION !!!!!)
        tradable only when spx is open position
        """
        
        gen_position_opened_date_from_trades(trade_csv=trade_file, open_date_csv=path_tradable_days)
        

gen_tradable_days(
    start_date=START_DATE, 
    end_date=END_DATE, 
    trade_file=path_spx_open_position_csv, 
    path_tradable_days=PATH_TRADABLE_DAYS,
    use_trade_position_open_days=use_trade_position_open_days
)


# validate
df = pd.read_csv(PATH_TRADABLE_DAYS)
l = len(df)
print(f'tradable {l} days')
