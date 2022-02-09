import pandas as pd

base_folder = 'D:/f_data/batch_20211116_strat_param_swing_2150in_2150out_ma_gap_no_take_profit/'
all_trades = base_folder + 'step8_portfolio_time_series/intermediate_per_track_trades.csv'
sub_trades_path = 'D:/f_data/analysis/20220208_momenton/trades_split/'

df = pd.read_csv(all_trades)
tickers = df['ticker'].unique()
assert len(tickers) == len(set(tickers))

total = 0
for ticker in tickers:
    print(ticker)
    df_sub = df[df['ticker']==ticker]
    total = total + len(df_sub)
    sub_csv = sub_trades_path + ticker + '.csv'
    df_sub.to_csv(sub_csv, index=False)
    
assert len(df) == total