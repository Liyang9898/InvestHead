from datetime import datetime
from math import nan

from batch_20201214.util_for_batch.batch_util import get_all_files
from operation.lib.trade_lib import batch_tradable, get_opened_position, \
    update_record_current_price, tradable
import pandas as pd
import pandas as pd
from trading_floor.EntryPointGenerator import gen_entry
from strategy_lib.strat_ma_swing import StrategySimpleMA
from strategy_lib.stratage_param import (
    strat_param_swing
)
from version_master.version import op_path_base, op_record


now = datetime.today()
now_str = now.strftime('%Y-%m-%d')

path_base = op_path_base + now_str
op_path_indicator = path_base + '/indicator/'
# new_record = update_record_current_price(op_path_indicator)



def test_entry_on_selected_day(ticker, target_date):
    path = op_path_indicator+ticker+'_downloaded_raw.csv'
    
    df = pd.read_csv(path)
    
    strategy_param_bundle=strat_param_swing
    idx = 0
    while idx < len(df):
        date = df.loc[idx, 'date']
        if target_date == date:
            break
        idx += 1
    #     print(date)
    print('pos=',idx)
    
    strategy=StrategySimpleMA(strategy_param_bundle)
    
    entry_info = gen_entry(df, idx, strategy)
    # entry_info = tradable(df, strategy_param_bundle, idx)
    print(entry_info)
    bar_yesterday = df.loc[idx-1]
    # bar_yesterday['ema8_delta'] > 0 and bar_yesterday['ema21_delta'] > 0 and bar_yesterday['ma50_delta'] > 0
    print(bar_yesterday['ema8_delta'], bar_yesterday['ema21_delta'],bar_yesterday['ma50_delta'])
    # bar_yesterday['ema21_ma50_MACD'] > 0
    print(bar_yesterday['ema21_ma50_MACD'])
    # bar_yesterday['ema21'] > bar_yesterday['ma50']
    print(bar_yesterday['ema21'] , bar_yesterday['ma50'])
    
    
ticker = 'AZPN'
target_date = '2021-03-10'
test_entry_on_selected_day(ticker, target_date)