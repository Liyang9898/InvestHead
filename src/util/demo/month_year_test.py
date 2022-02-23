    

import pandas as pd
from util.general_ui import plot_bars_from_xy_list
from util.util_pandas import percent_increase_of_current_row
from util.util_time import extract_period_start_from_df, PERIOD_CALENDAR_YEAR,\
    PERIOD_CALENDAR_MONTH


path = 'D:/f_data/batch_20211116_different_stock_pick/random/baseball_card_position_time_series.csv'

# path = 'D:/f_data/batch_20211116_different_stock_pick/top_return/baseball_card_position_time_series.csv'


def gen_vs_benchmark(timeseries_path, col_date, col_benchmark, col_portfolio):
    df = pd.read_csv(timeseries_path)
    df = extract_period_start_from_df(df, col_date, PERIOD_CALENDAR_YEAR)
    
    
    percent_increase_of_current_row(df, col_benchmark)
    percent_increase_of_current_row(df, col_portfolio)
    df['after_hedge'] = df['portfolio_pct_increase'] - df['SPY_pct_increase']
    # print(df[['date','portfolio_pct_increase','SPY_pct_increase','after_hedge']])
    
    df_p = df[df['after_hedge']>0]
    df_n = df[df['after_hedge']<0]
    print(len(df_p)/(len(df_p)+len(df_n)), df_p['after_hedge'].sum(), df_n['after_hedge'].sum())
    win_pnl = round(df_p['after_hedge'].sum(), 2)
    lose_onl = round(df_n['after_hedge'].sum(), 2)
    win_potion = round(len(df_p)/(len(df_p)+len(df_n)), 2)
    
    title = f'PNL vs benchmark per year, win_potion={win_potion}%, win_pnl={win_pnl}%, lose_onl={lose_onl}%'
    plot_bars_from_xy_list(x_list=df['date'].to_list(), y_list=df['after_hedge'].to_list(), title=title, path=None)
    
    
gen_vs_benchmark(
    timeseries_path=path, 
    col_date='date', 
    col_benchmark='SPY', 
    col_portfolio='portfolio'
)