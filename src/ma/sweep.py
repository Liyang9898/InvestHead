'''
Created on Feb 1, 2020

@author: leon
'''


from download_stock.all_ticker import create_list_of_filepaths
from ma.addindicator import load_df_add_indicator
from ma.gentrade import gen_trades_always_in, trade_summary, \
    gen_trade_summary_raw, gen_trade_summary, print_trades
from ma.improve_trade import improve_entry_and_exit
from ma.plotindicator import plot_symbol
import pandas as pd


# import plotly.graph_objects as go
ma_indicator = 'sequence_8_21'
# ma_indicator = 'sequence_8_21_50'


filename = 'BATS_TWTR, 1D'
filenames = [
    'BATS_TWTR, 1D',
    'BATS_AMZN, 1D',
    'BATS_GOOG, 1D',
    'BATS_MSFT, 1D',
    'BATS_NVDA, 1D',
    'BATS_AMD, 1D',
    'BATS_UBER, 1D',
    'BATS_LYFT, 1D',
    'BATS_TSLA, 1D',
    'BATS_BILI, 1D',
    'BATS_PINS, 1D',
    'BATS_SNAP, 1D',
    'BATS_BYND, 1D',
    'BATS_SQ, 1D',
    'BATS_NFLX, 1D',
    'BATS_AAPL, 1D'
]
path_out = """D:/f_data/swing_multi_stock.csv"""

path_in = """D:/f_data/{file_name}.csv""".format(file_name=filename)

def single_stock_run(ticker):
#     path_in = """D:/f_data/{file_name}.csv""".format(file_name=filename)
    path_in = """D:/f_data/download_yfinance/{ticker}_download_format.csv""".format(ticker=ticker)

    df_with_indicator = load_df_add_indicator(path_in, '2017-01-01', '2020-02-13')

     
    trades = gen_trades_always_in(df_with_indicator, ma_indicator)    
    sum = gen_trade_summary_raw(trades)
    print(sum)
    
    OVERLAP_EMA21 = 'price overlap ema21'
    BELOW_ENTRY = 'x% below entry'
    HALF_MAX = 'drop to x% of max reach'
    BREACH_RETURN = 'drop to entry after breach'
    JUMP_RETURN = 'drop to entry after breach jump over'
     
    SPEED = 'speed_ema8'
    NEAR = 'near_ema8'
    
    
    trades_improved = improve_entry_and_exit(
        df_day=df_with_indicator, 
        trades=trades, 
        # enter params
        start_v=0.02,  # must adjust according to stock!!! 
        distance=0.05,
        # exit params
        threshold_below_entry=0.05, 
        breach_threshold_above_entry=0.05,  # must adjust according to stock!!! 
        bar_count_threshold=11, 
        max_reach_drop_percent=0.5,
        enter_impro_strat=[
    #         SPEED,
    #         NEAR
        ],
        exit_impro_strat=[
            OVERLAP_EMA21,
    #         BELOW_ENTRY,
    #         HALF_MAX,
    #         BREACH_RETURN
        ]
    )
    
    sum_improved = gen_trade_summary(trades_improved)
    print(sum_improved)
    
    
    
    trades_improved_profit_managed = improve_entry_and_exit(
        df_day=df_with_indicator, 
        trades=trades, 
        # enter params
        start_v=0.02,  # must adjust according to stock!!! 
        distance=0.05,
        # exit params
        threshold_below_entry=0.05, 
        breach_threshold_above_entry=0.025,  # must adjust according to stock!!! 
        bar_count_threshold=11, 
        max_reach_drop_percent=0.5,
        enter_impro_strat=[
    #         SPEED,
    #         NEAR
        ],
        exit_impro_strat=[
            OVERLAP_EMA21,
    #         BELOW_ENTRY,
    #         HALF_MAX,
            BREACH_RETURN
        ]
    )
    
    print('============================improved,  profit managed==============================')
    sum_improved_profit_managed = gen_trade_summary(trades_improved_profit_managed)
    print(sum_improved_profit_managed)
    

    res = {
        'stock':ticker,
        'win':sum_improved_profit_managed['win rate'],
        'lose':sum_improved_profit_managed['lose rate'],
        'total_trades':sum_improved_profit_managed['total trades'],
        'pnl':sum_improved_profit_managed['pnl'],
        'win_raw':sum_improved['win rate'],
        'lose_raw':sum_improved['lose rate'],
        'pnl_raw':sum_improved['pnl'],
    }
    return res


def sweep(tickers, path_out):
    cnt = 1
    res = []
    for ticker in tickers:
#         if cnt > 2500 and cnt < 2510:
        print(str(cnt)+' processing:' + ticker)
        a = single_stock_run(ticker)
        res.append(a)
        cnt = cnt + 1

     
#     print(res)
    df = pd.DataFrame(data=res)
    print(df)
    df.to_csv(path_out,columns =['stock','win','lose','total_trades','pnl','win_raw','lose_raw','pnl_raw'], index=False)
    print('sweep csv done')
    
ticker = create_list_of_filepaths()
path_out = """D:/f_data/swing_all_stock_20200209.csv"""
sweep(ticker, path_out)