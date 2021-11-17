import pandas as pd

from trading_floor.EntryPointGenerator import gen_entry
from strategy_lib.strat_ma_swing import StrategySimpleMA
from batch_20201214.util_for_batch.batch_util import get_all_files
# from version_master.version import op_path_indicator
from version_master.version import op_path_base
from datetime import datetime
from version_master.version import op_path_base, op_record
from datetime import datetime
BELOW_ENTER='BELOW_ENTER'
ABOVE_STOP='ABOVE_STOP'
BETWEEN_STOP_ENTER='BETWEEN STOP-ENTER---SELL'
ABOVE_ENTER_NO_STOP='ABOVE_ENTER_NO_STOP'

now = datetime.today()

now_str = now.strftime('%Y-%m-%d')

path_base = op_path_base + now_str
op_path_indicator = path_base + '/indicator/'

def check_macd():
    # this method go over all opened position
    
    # part 1
    # check yesterday's MA
    # to see if ema21 is under ma50

    # part 2
    # current price can be categorized into 3 sections:
    # 1. BELOW_ENTER.  
    # 2. ABOVE_STOP   
    # 3. BETWEEN STOP-ENTER  ---SELL
    # 4. ABOVE_ENTER_NO_STOP
    cnt = 0
    macd_cnt = 0
    res = {}
    macd_bad_ticker = []
    record_path = op_record
    record_df = pd.read_csv(record_path)
    for i in range(0, len(record_df)):
        ticker = record_df.loc[i, 'ticker'].lower()
        enter_time = record_df.loc[i, 'date']
        datetime_object = datetime.strptime(enter_time, '%m/%d/%Y')
        enter_time = datetime_object.strftime("%Y-%m-%d")
#         print(enter_time)
#         current_rate = record_df.loc[i,'current_rate']
#         status = record_df.loc[i, 'status']
#         if status in ['win', 'lose', 'neutral']:
#             # skip closed position
#             continue
#         enter_price = record_df.loc[i, 'enter_price']
#         a_stop_price = record_df.loc[i, 'a_stop_price']
        
        
        # get indicator file
        price_path = op_path_indicator + ticker + '_downloaded_raw.csv'
        try:
            ticker_df = pd.read_csv(price_path)
        except:
            print(ticker, 'has no stock data')
            continue

        idx = ticker_df[ticker_df['date'] == enter_time].index.values[0]-1
        
        macd = ticker_df.loc[idx, 'ema21_ma50_MACD']
        date = ticker_df.loc[idx + 1, 'date']
#         bar_yesterday['ema21_ma50_MACD'] > 0
        cnt = cnt + 1
        if macd > 0:
            macd_cnt = macd_cnt + 1
        else:
            macd_bad_ticker.append(ticker)
        print(ticker,date, macd)
    print(cnt,macd_cnt)    
    print(macd_bad_ticker)
        
a = check_macd()
