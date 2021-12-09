from datetime import datetime

from api.api import api_download_ticker, api_position_perf_from_csv, \
    api_compuate_alpha_beta_to_csv_img
from batch_20211116.batch_20211116_lib.constant import PORTFOLIO_TIME_SERIES_FOLDER_RUSSLL1000, \
    ANALYSIS_START_DATE, END_DATE, CONCLUSION_FOLDER, BENCHMARK_TICKER
import pandas as pd
from util.general_ui import plot_bars_from_xy_list, plot_points_from_xy_list


def get_benchmark(ticker):
    start = ANALYSIS_START_DATE
    end = END_DATE
    interval = '1d'

    path = 'D:/f_data/temp/spy20211207.csv'
    api_download_ticker(ticker, start, end, path, interval)
    df = pd.read_csv(path)
    
    df['date']=df.apply(lambda row : str(datetime.fromtimestamp(int(row['unixtime'])).strftime('%Y-%m-%d')), axis = 1)
    df[BENCHMARK_TICKER] = df['Close']
    base = df.loc[0,BENCHMARK_TICKER]
    df[BENCHMARK_TICKER] = df[BENCHMARK_TICKER] / base
    df=df[['date',BENCHMARK_TICKER]]
    df=df.copy()
    return df

# get benchmark data
df_benchmark = get_benchmark(BENCHMARK_TICKER)

# merge with trade results
result_position_path = PORTFOLIO_TIME_SERIES_FOLDER_RUSSLL1000 + 'position.csv'
df_result_position = pd.read_csv(result_position_path)
m_result = pd.merge(df_result_position, df_benchmark, how="inner", on="date")
path_position_with_benchmark = CONCLUSION_FOLDER + 'intermediate_position_with_benchmark.csv'
m_result.to_csv(path_position_with_benchmark, index=False)

# position perf
perf_output_path_main = CONCLUSION_FOLDER + 'intermediate_position_perf_potofolio.csv'
api_position_perf_from_csv(
    position_path=path_position_with_benchmark, 
    start_date=ANALYSIS_START_DATE, 
    end_date=END_DATE, 
    date_col='date', 
    position_col='roll',
    perf_output_path=perf_output_path_main
)  

perf_output_path_benchmark = CONCLUSION_FOLDER + 'intermediate_position_perf_spy_benchmark.csv'
api_position_perf_from_csv(
    position_path=path_position_with_benchmark, 
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

# alpha beta monthly yearly
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
until here, we have alpha beta for monthly and yearly 
"""



# x_list = m_result['date'].to_list()
# y_list = {'roll':m_result['roll'].to_list(),'spy':m_result['spy'].to_list()}
# plot_points_from_xy_list(x_list, y_list)
# print(m_result)


# todo
# compare with spy 
# alpha, beta, align 
# win rate, win_lose_pnl_ratio, 
# -------------
# 4% not take profit, upper ma gap select