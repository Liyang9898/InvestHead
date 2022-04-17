from datetime import datetime, timedelta

from batch_20201214.util_for_batch.batch_util import get_all_files
import pandas as pd
from util.util_finance_chart import plot_candle_stick_with_trace
from version_master.version import op_path_base, swing_set_2019_2022


def gen_exit(df):
    """
    max_drop_threshold=-1 means a position return to 0 and lost all
    """
    
    df.reset_index(inplace=True, drop=True)
    x = []
    y = []

    for i in range(0, len(df)):
        ts =  df.loc[i, 'est_datetime']
        ma50 = df.loc[i, 'ma50']
        ema21 = df.loc[i, 'ema21']
        close = df.loc[i, 'close']
            
        if ema21<ma50:
            x.append(ts)
            y.append(close)
            
    exit = {
        'x':x,
        'y':y
    }
    return exit


def scan_exit_single_st(ticker, plot=False):
    # pull df
    now = datetime.today()
    now_str = now.strftime('%Y-%m-%d')
    path_base = op_path_base + now_str
    op_path_indicator = path_base + '/indicator/'
    ticker = ticker.upper()
    idc_path = op_path_indicator + ticker + '_downloaded_raw.csv'
    df = pd.read_csv(idc_path)

    # apply trace
    exit = gen_exit(df)
    exit_ts = exit['x']
    traces = {
        'exit': exit
    } 
    
    # plot 
    if plot:
        title = ticker
        plot_candle_stick_with_trace(
            df, 
            traces,
            title
        )
        
    # check yesterday
    previous_ts = df.loc[len(df)-2, 'est_datetime']

    if previous_ts in exit_ts:
        return True
    else:
        return False
    
    
def get_opened_ticker_list():
    """
    testing start
    """
    # now = datetime.today()
    # now_str = now.strftime('%Y-%m-%d')
    # path_base = op_path_base + now_str
    # op_path_indicator = path_base + '/indicator/'
    #
    # path_files = get_all_files(op_path_indicator)
    # ticker_list = list(path_files.keys())
    # return ticker_list
    """
    testing end
    """
    path_record = op_path_base+'record.csv'
    df = pd.read_csv(path_record)
    ticker_list = df['ticker'].to_list()
    print('ticker list:', ticker_list)
    return ticker_list
    

def scan_all_exit():
    ticker_list = get_opened_ticker_list()
    exit_list = []
    not_exit_list = []
    for ticker in ticker_list:
        should_exit = scan_exit_single_st(ticker)
        if should_exit:
            exit_list.append(ticker)
            print('Should exit? ', ticker, should_exit)
        else:
            not_exit_list.append(ticker)
    print('exit', len(exit_list), 'not exit', len(not_exit_list))


scan_all_exit()