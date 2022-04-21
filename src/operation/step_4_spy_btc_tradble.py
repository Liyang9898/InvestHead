
import pandas as pd
from price_asset_master.lib.refresh_price_asset_add_indicator import refresh_price_asset_add_indicator
from util.util_finance_chart import plot_candle_stick_with_trace
from datetime import datetime

from operation.lib.trade_lib import batch_tradable
import pandas as pd
from strategy_lib.stratage_param import strat_param_20211006_ma_max_drawdown_cut, \
    strat_param_20211006_ma_macd
from util.util_finance_chart import plot_candle_stick_with_trace
from util.util_time import get_today_date_str
from global_constant.global_constant import root_path
from _socket import close



def gen_exit(df):
    """
    max_drop_threshold=-1 means a position return to 0 and lost all
    """
    
    df.reset_index(inplace=True, drop=True)

    x = []
    y = []
    # max = 0
    for i in range(0, len(df)):
        ts =  df.loc[i, 'est_datetime']
        ma50 = df.loc[i, 'ma50']
        ema21 = df.loc[i, 'ema21']
        close = df.loc[i, 'close']
        # if close > max:
        #     max = close
        # else:
        #     drop_pct = close / max - 1
            
        if ema21<ma50:
            x.append(ts)
            y.append(close)
            
    exit = {
        'x':x,
        'y':y
    }
    return exit


def spy_enterable():
    date_str = get_today_date_str()
    path_base=f'{root_path}/operation_spy/{date_str}/indicator/'
    idc_path = path_base + 'spy_downloaded_raw.csv'
    df_spy_idc = pd.read_csv(idc_path)
    
    strategy_param_bundle=strat_param_20211006_ma_max_drawdown_cut
    offset=0
    
    possible_entry = batch_tradable(
        path_base, 
        strategy_param_bundle,
        offset
    )
    print(f'possible entry for SPY today {date_str}:', len(possible_entry))
    
    
    # make charts
    x = []
    y = []
    for offset in range(0,100):
        possible_entry = batch_tradable(
            path_base, 
            strategy_param_bundle,
            offset
        )
        if len(possible_entry) > 0:
            entry_info = possible_entry['spy']['entry_info']
            entry_ts = entry_info['entry_ts']
            entry_price = entry_info['entry_price']
            x.append(entry_ts)
            y.append(entry_price)
            
    exit = gen_exit(df_spy_idc)   
    traces = {
        'enter': {
            'x':x,
            'y':y
        },
        'exit': exit
    } 
    
    enter_str = 'ENTER: NO'
    previous_bar_ts = df_spy_idc.loc[len(df_spy_idc) - 2, 'est_datetime']
    enterable_date = traces['enter']['x']
    if previous_bar_ts in enterable_date:
        enter_str = 'ENTER: YES'
    
    title = 'SPY today:' + date_str + ' need to check last bar, not current bar!!!!              ' + enter_str
    plot_candle_stick_with_trace(
        df_spy_idc, 
        traces,
        title
    )


def btc_enterabe():
    date_str = get_today_date_str()
    path_base=f'{root_path}/operation_btc/{date_str}/indicator/'
    idc_path = path_base + 'BTC-USD_downloaded_raw.csv'
    df_idc = pd.read_csv(idc_path)
    
    strategy_param_bundle=strat_param_20211006_ma_macd
    offset=0
    
    possible_entry = batch_tradable(
        path_base, 
        strategy_param_bundle,
        offset
    )
    print(f'possible entry for BTC today {date_str}:', len(possible_entry))
    
    
    # make charts
    x = []
    y = []
    for offset in range(0,100):
        possible_entry = batch_tradable(
            path_base, 
            strategy_param_bundle,
            offset
        )
        if len(possible_entry) > 0:
            entry_info = possible_entry['btc-usd']['entry_info']
            entry_ts = entry_info['entry_ts']
            entry_price = entry_info['entry_price']
            x.append(entry_ts)
            y.append(entry_price)
         
    
    exit = gen_exit(df_idc)   
    traces = {
        'enter': {
            'x':x,
            'y':y
        },
        'exit': exit
    } 
    
    
    enter_str = 'ENTER: NO'
    previous_bar_ts = df_idc.loc[len(df_idc) - 2, 'est_datetime']
    enterable_date = traces['enter']['x']
    if previous_bar_ts in enterable_date:
        enter_str = 'ENTER: YES'
    
    title = 'BTC today:' + date_str + ' need to check last bar, not current bar!!!!              ' + enter_str
    plot_candle_stick_with_trace(
        df_idc, 
        traces,
        title
    )
    


print('====================================================================================================================')
btc_enterabe()
spy_enterable()
print('===================================================END=================================================================')

