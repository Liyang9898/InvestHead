from datetime import datetime
import random

from api.api import api_download_ticker, api_position_perf_from_csv, \
    api_compuate_alpha_beta_to_csv_img, api_trade_perf_from_trades_csv
from batch_20220207.batch_20220207_lib.constant import BENCHMARK_TICKER
from batch_20220207.batch_20220207_lib.util_batch_simulation import position_time_series_append_benchmark_to_csv_png, \
    strategy_baseball_card
import pandas as pd
from util.general_ui import plot_bars_from_xy_list, plot_points_from_xy_list
from util.util_time import date_formatter_1


# preprocess position line
position_raw_path = 'D:/f_data/batch_20220207_spy/step8_portfolio_time_series/position_list_temp.csv'
position_path = 'D:/f_data/batch_20220207_spy/step8_portfolio_time_series/position.csv'
position_raw_df = pd.read_csv(position_raw_path)
position_raw_df['roll'] = position_raw_df['experiment']
position_raw_df = position_raw_df[['date', 'roll']].copy()
position_raw_df.to_csv(position_path, index=False)


CONCLUSION_FOLDER = 'D:/f_data/batch_20220207_spy/step9_conclusion/'
PORTFOLIO_TIME_SERIES_FOLDER_RUSSLL1000 = 'D:/f_data/batch_20220207_spy/step8_portfolio_time_series/'
ANALYSIS_START_DATE = "1958-01-01"
END_DATE = '2022-01-01'

# position time series
result_position_path = PORTFOLIO_TIME_SERIES_FOLDER_RUSSLL1000 + 'position.csv'
path_position_with_benchmark_csv = CONCLUSION_FOLDER + 'baseball_card_position_time_series.csv'
path_position_with_benchmark_png = CONCLUSION_FOLDER + 'baseball_card_position_time_series.png'
position_time_series_append_benchmark_to_csv_png(
    position_time_series_csv=result_position_path,
    input_time_col='date',
    input_position_col='roll',
    start_date=ANALYSIS_START_DATE,
    end_date=END_DATE,
    benchmark_ticker='SPY',
    output_time_series_csv=path_position_with_benchmark_csv,
    output_time_series_png=path_position_with_benchmark_png
)
"""
until here you have position time series and benchmarh save in a csv and png together
"""
 
# position perf
perf_output_path_main = CONCLUSION_FOLDER + 'intermediate_position_perf_potofolio.csv'
api_position_perf_from_csv(
    position_path=path_position_with_benchmark_csv, 
    start_date=ANALYSIS_START_DATE, 
    end_date=END_DATE, 
    date_col='date', 
    position_col='portfolio',
    perf_output_path=perf_output_path_main
)  
 
perf_output_path_benchmark = CONCLUSION_FOLDER + 'intermediate_position_perf_spy_benchmark.csv'
api_position_perf_from_csv(
    position_path=path_position_with_benchmark_csv, 
    start_date=ANALYSIS_START_DATE, 
    end_date=END_DATE, 
    date_col='date', 
    position_col=BENCHMARK_TICKER,
    perf_output_path=perf_output_path_benchmark
)  
df_perf_main = pd.read_csv(perf_output_path_main)
df_perf_bench = pd.read_csv(perf_output_path_benchmark)
df_perf_main['ticker'] = 'portfolio'
df_perf_bench['ticker'] = BENCHMARK_TICKER
df_merge = pd.concat([df_perf_main, df_perf_bench])
perf_merge_output_path = CONCLUSION_FOLDER + 'position_perf.csv'
df_merge.to_csv(perf_merge_output_path, index=False)
"""
until here we have position perf: return, sharpe
"""
 
 
"""
monthly alpha beta
"""
api_compuate_alpha_beta_to_csv_img(
    position_csv=result_position_path, 
    date_col='date', 
    position_col='roll', 
    start_date=ANALYSIS_START_DATE, 
    end_date=END_DATE, 
    benchmark_ticker=BENCHMARK_TICKER,
    period='month',
    result_path=CONCLUSION_FOLDER
)
 
 
"""
yearly alpha beta
"""
api_compuate_alpha_beta_to_csv_img(
    position_csv=result_position_path, 
    date_col='date', 
    position_col='roll', 
    start_date=ANALYSIS_START_DATE, 
    end_date=END_DATE, 
    benchmark_ticker=BENCHMARK_TICKER,
    period='year',
    result_path=CONCLUSION_FOLDER
)
 
 
"""
trade perf, win rate, win_lose_pnl_ratio, trade count
"""
trades_csv = f'{PORTFOLIO_TIME_SERIES_FOLDER_RUSSLL1000}intermediate_per_track_trades.csv'
output_perf_csv = f'{CONCLUSION_FOLDER}/trade_perf.csv'
api_trade_perf_from_trades_csv(trades_csv, output_perf_csv)
 
strategy_baseball_card(
    position_perf_csv=perf_merge_output_path,
    trade_perf_csv=output_perf_csv,
    year_alpha_beta_csv=CONCLUSION_FOLDER+'year_alpha_beta.csv',
    month_alpha_beta_csv=CONCLUSION_FOLDER+'month_alpha_beta.csv',
    baseball_card_csv=CONCLUSION_FOLDER+'baseball_card_strategy_perf.csv',
)
 
# # x_list = m_result['date'].to_list()
# # y_list = {'roll':m_result['roll'].to_list(),'spy':m_result['spy'].to_list()}
# # plot_points_from_xy_list(x_list, y_list)
# # print(m_result)
# 
# 
# # todo
# # compare with spy 
# # alpha, beta, align 
# # win rate, win_lose_pnl_ratio, 
# # -------------
# # 4% not take profit, upper ma gap select