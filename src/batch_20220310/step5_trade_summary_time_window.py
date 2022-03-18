from api.api import api_gen_trade_summary
from batch_20220310.batch_20220310_lib.constant import RAWS_TRADES_FOLDER_COLLECTION_OF_ALL_TIME, trade_all_entry_path, \
    trade_consecutive_path, indicator_path, \
    trade_summary_per_ticker_path, trade_summary_all_ticker_path, \
    gen_time_window, WINDOW_SIZE, START_YEAR, END_YEAR, START_DATE, END_DATE
import pandas as pd
from util.util_file import get_all_csv_file_in_folder
from util.util_time import df_filter_dy_date
import os


# start_date = START_DATE
# end_date = END_DATE

"""
This process does this:
For each year, we do compute the historical trade perf of the past 2 year for all stock
Input:
    trades
Output:
    each file is a year. Each file has all stock's perf in past 3 years.
    file name is the perf's observation time rage
"""

def gen_ma50_up_date(
    indicator_file,
    start_date,
    end_date
):
    df = pd.read_csv(indicator_file)
    df = df_filter_dy_date(df,'date',start_date,end_date)
    df_up = len(df[df['ma50_delta'] > 0])
    df_down = len(df[df['ma50_delta'] < 0])
    rate = 0
    if df_up + df_down > 0:
        rate = df_up / (df_up + df_down)
    return rate


def all_tickers_trade_summary_in_time_window(
    start_date, 
    end_date,
):
    """
    given a folder of indicator and trades,
    output: one csv of trade summary, one row one stock
    """
    summary_path_all_ticker = trade_summary_all_ticker_path(start_date, end_date)
    if os.path.isfile(summary_path_all_ticker):
        print(summary_path_all_ticker, 'exist, skip')
        return
    
    cnt = 0
    
    # get all tickers from trades file
    raw_files = get_all_csv_file_in_folder(RAWS_TRADES_FOLDER_COLLECTION_OF_ALL_TIME)
    tickers = []
    for file in raw_files:
        file = file.replace('.csv', '')
        tokens = file.split('/')
        file_name = tokens[-1]
        ticker = file_name.split('_')[0]
        if ticker not in tickers:
            tickers.append(ticker)

    rows =[]
    for ticker in tickers:
        print(cnt, ticker, start_date, end_date)
        all_entry_path = trade_all_entry_path(ticker)
        consecutive_path = trade_consecutive_path(ticker)
        price_indicator_path = indicator_path(ticker)
        summary_path_per_ticker = trade_summary_per_ticker_path(ticker, start_date, end_date)
        
        
        # process indicator
        df_indicator = pd.read_csv(price_indicator_path)
        ma50_up_rate = gen_ma50_up_date(
            indicator_file = price_indicator_path,
            start_date=start_date, 
            end_date=end_date,
        )
        
        # process trades
        api_gen_trade_summary(
            trade_result_all_entry_path=all_entry_path,
            trade_result_consecutive_entry_path=consecutive_path,
            trade_summary_path=summary_path_per_ticker,
            start_date=start_date, 
            end_date=end_date, 
        )
        df_summary = pd.read_csv(summary_path_per_ticker)
        dict_summary = df_summary.to_dict('records')[0]
        
        total_trades_consecutive = dict_summary['total_trades']
        days_with_price = len(df_indicator)
        if total_trades_consecutive <= 0 or days_with_price <= 0:
            cnt += 1
            continue
        
        row = {
            'ticker': ticker,
            'ma50_up_rate': ma50_up_rate,
            'win_rate': dict_summary['key_metric_win_rate'],
            'annual_avg_return': dict_summary['key_metric_annual_avg_return'],
            'win_lose_pnl_ratio': dict_summary['key_metric_win_lose_pnl_ratio'],
            'total_trades_all_entry': dict_summary['all_universe_total_trades']
        }
        rows.append(row)
        
        cnt += 1
#         if cnt > 5:
#             break

    
    df_all_ticker_perf = pd.DataFrame(rows)
    df_all_ticker_perf.to_csv(summary_path_all_ticker, index=False)
    return


windows = gen_time_window(window_size=WINDOW_SIZE, start_year=START_YEAR, end_year=END_YEAR) 

for window in windows:
    all_tickers_trade_summary_in_time_window(
        start_date=window['start'], 
        end_date=window['end'],
    )
