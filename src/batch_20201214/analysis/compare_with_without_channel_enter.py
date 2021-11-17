'''
Created on Jan 27, 2021

@author: leon
'''
import pandas as pd

folder_path_trade_results = "D:/f_data/sweep_20201214/trade_result/20210126_21_50_channel_controlled_enter/"
folder_path_price_with_indicator = "D:/f_data/sweep_20201214/indicator_stock_20210124/"
ticker_list = "D:/f_data/sweep_20201214/conclusion_filtered/20200113_filter_vol_1m_cap_03b_80winrate_10trade.csv"

channel_enter_swing_path = "D:/f_data/sweep_20201214/conclusion_20210126/20210126_21_50_channel_controlled_enter.csv"
swing_path = "D:/f_data/sweep_20201214/conclusion_20210108/trades_summary_ma21_50_with_profit_manage_no_neutral_out_20210117.csv"

df_with_channel = pd.read_csv(channel_enter_swing_path)
df_without_channel = pd.read_csv(swing_path)



def retain_cols(df, cols):
    for c in df.columns:
        if c not in cols:
            del df[c]

df_without_channel['all_universe_win_rate_without_ch']=df_without_channel['all_universe_win_rate']
df_without_channel['total_trades_without_ch']=df_without_channel['total_trades']
df_without_channel['win_pnl_p_without_ch']=df_without_channel['win_pnl_p']
df_without_channel['lose_pnl_p_without_ch']=df_without_channel['lose_pnl_p']
df_without_channel['total_pnl_fix_without_ch']=df_without_channel['total_pnl_fix']
df_without_channel['total_pnl_rollover_without_ch']=df_without_channel['total_pnl_rollover']

retain_cols(
    df_without_channel,
    [
        'ticker',
        'all_universe_win_rate_without_ch',
        'total_trades_without_ch',
        'win_pnl_p_without_ch',
        'lose_pnl_p_without_ch',
        'total_pnl_fix_without_ch',
        'total_pnl_rollover_without_ch'
    ]
)

df_with_channel['all_universe_win_rate_with_ch']=df_with_channel['all_universe_win_rate']
df_with_channel['total_trades_with_ch']=df_with_channel['total_trades']
df_with_channel['win_pnl_p_with_ch']=df_with_channel['win_pnl_p']
df_with_channel['lose_pnl_p_with_ch']=df_with_channel['lose_pnl_p']
df_with_channel['total_pnl_fix_with_ch']=df_with_channel['total_pnl_fix']
df_with_channel['total_pnl_rollover_with_ch']=df_with_channel['total_pnl_rollover']

retain_cols(
    df_with_channel,
    [
        'ticker',
        'all_universe_win_rate_with_ch',
        'total_trades_with_ch',
        'win_pnl_p_with_ch',
        'lose_pnl_p_with_ch',
        'total_pnl_fix_with_ch',
        'total_pnl_rollover_with_ch'
    ]
)


df_with_channel['all_universe_win_rate_diff']=df_with_channel['all_universe_win_rate_with_ch']-df_without_channel['all_universe_win_rate_without_ch']
df_with_channel['total_trades_diff']=(df_with_channel['total_trades_with_ch']-df_without_channel['total_trades_without_ch'])/df_without_channel['total_trades_without_ch']
df_with_channel['win_pnl_p_diff']=(df_with_channel['win_pnl_p_with_ch']-df_without_channel['win_pnl_p_without_ch'])/df_without_channel['win_pnl_p_without_ch']
df_with_channel['lose_pnl_p_diff']=(df_with_channel['lose_pnl_p_with_ch']-df_without_channel['lose_pnl_p_without_ch'])/df_without_channel['lose_pnl_p_without_ch']
df_with_channel['total_pnl_fix_diff']=(df_with_channel['total_pnl_fix_with_ch']-df_without_channel['total_pnl_fix_without_ch'])/df_without_channel['total_pnl_fix_without_ch']
df_with_channel['total_pnl_rollover_diff']=(df_with_channel['total_pnl_rollover_with_ch']-df_without_channel['total_pnl_rollover_without_ch'])/df_without_channel['total_pnl_rollover_without_ch']


print(df_without_channel.head())
print(df_with_channel.head())

res = pd.merge(df_without_channel, df_with_channel, on="ticker")

# DIFF COLUMNS


print(res)
output = "D:/f_data/sweep_20201214/analysis_20210127/compare_with_without_channel_enter.csv"
res.to_csv(output, index = False)

iwf200 = "D:/f_data/sweep_20201214/edit/csv/20210117_2b_1m_10trade_60win_positive_iwf.csv"
iwf200_df=pd.read_csv(iwf200)
iwf_ticker_list=iwf200_df['ticker'].to_list()
res_iwf_only=res.loc[res['ticker'].isin(iwf_ticker_list)]
output_iwf_only="D:/f_data/sweep_20201214/analysis_20210127/compare_with_without_channel_enter_iwf.csv"
res_iwf_only.to_csv(output_iwf_only, index = False)

print(res_iwf_only)