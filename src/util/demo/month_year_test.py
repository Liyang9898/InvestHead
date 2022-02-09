    

import pandas as pd
from util.general_ui import plot_bars_from_xy_list
from util.util_pandas import percent_increase_of_current_row
from util.util_time import extract_period_start_from_df, PERIOD_CALENDAR_YEAR,\
    PERIOD_CALENDAR_MONTH


# path = 'D:/f_data/batch_20211116_different_stock_pick/random/baseball_card_position_time_series.csv'

path = 'D:/f_data/batch_20211116_different_stock_pick/top_return/baseball_card_position_time_series.csv'


df = pd.read_csv(path)
df = extract_period_start_from_df(df, 'date', PERIOD_CALENDAR_YEAR)


percent_increase_of_current_row(df, 'SPY')
percent_increase_of_current_row(df, 'portfolio')
df['after_hedge'] = df['portfolio_pct_increase'] - df['SPY_pct_increase']
# print(df[['date','portfolio_pct_increase','SPY_pct_increase','after_hedge']])

df_p = df[df['after_hedge']>0]
df_n = df[df['after_hedge']<0]
print(len(df_p)/(len(df_p)+len(df_n)), df_p['after_hedge'].sum(), df_n['after_hedge'].sum())
plot_bars_from_xy_list(x_list=df['date'].to_list(), y_list=df['after_hedge'].to_list(), title='default', path=None)