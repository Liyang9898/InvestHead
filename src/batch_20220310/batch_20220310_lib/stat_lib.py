from datetime import datetime
import random
import os

from api.api import api_download_ticker, api_position_perf_from_csv, \
    api_compuate_alpha_beta_to_csv_img, api_trade_perf_from_trades_csv
from batch_20220310.batch_20220310_lib.constant import PORTFOLIO_TIME_SERIES_FOLDER_COLLECTION, \
    ANALYSIS_START_DATE, END_DATE, CONCLUSION_FOLDER, BENCHMARK_TICKER
from batch_20220310.batch_20220310_lib.ui_multi_year_chart import gen_per_year_position_timeseries, \
    gen_vs_benchmark
from batch_20220310.batch_20220310_lib.util_batch_simulation import position_time_series_append_benchmark_to_csv_png, \
    strategy_baseball_card
import pandas as pd
from util.general_ui import plot_bars_from_xy_list, plot_points_from_xy_list


def gen_perf_stat_from_position_time_series(
    path_position_time_series, # requirement
    position_time_series_date_col,
    position_time_series_position_col,
    path_trades_csv,
    path_result_folder,
    benchmark_ticker,
    start_date, # can be automated TODO
    end_date,
    norgate=True
):
    ### INPUT ###
    result_position_path = path_position_time_series
    #############
    
    path_position_with_benchmark_csv = path_result_folder + 'baseball_card_position_time_series.csv'
    path_position_with_benchmark_png = path_result_folder + 'baseball_card_position_time_series.png'
     
    position_time_series_append_benchmark_to_csv_png(
        position_time_series_csv=result_position_path,
        input_time_col=position_time_series_date_col,
        input_position_col=position_time_series_position_col,
        start_date=start_date,
        end_date=end_date,
        benchmark_ticker=benchmark_ticker,
        output_time_series_csv=path_position_with_benchmark_csv,
        output_time_series_png=path_position_with_benchmark_png,
        norgate=norgate
    )
    print('until here you have position time series and benchmarh save in a csv and png together')
    """
    until here you have position time series and benchmarh save in a csv and png together
    """
    
    # position perf
    perf_output_path_main = path_result_folder + 'intermediate_position_perf_potofolio.csv'
    api_position_perf_from_csv(
        position_path=path_position_with_benchmark_csv, 
        start_date=start_date, 
        end_date=end_date, 
        date_col='date', 
        position_col='portfolio',
        perf_output_path=perf_output_path_main
    )  
    
    perf_output_path_benchmark = path_result_folder + 'intermediate_position_perf_benchmark.csv'
    api_position_perf_from_csv(
        position_path=path_position_with_benchmark_csv, 
        start_date=start_date, 
        end_date=end_date, 
        date_col='date', 
        position_col=benchmark_ticker,
        perf_output_path=perf_output_path_benchmark
    )  
    df_perf_main = pd.read_csv(perf_output_path_main)
    df_perf_bench = pd.read_csv(perf_output_path_benchmark)
    df_perf_main['ticker'] = 'portfolio'
    df_perf_bench['ticker'] = benchmark_ticker
    df_merge = pd.concat([df_perf_main, df_perf_bench])
    perf_merge_output_path = path_result_folder + 'position_perf.csv'
    df_merge.to_csv(perf_merge_output_path, index=False)
    print('until here we have position perf: return, sharpe')
    """
    until here we have position perf: return, sharpe
    """
    

    """
    monthly alpha beta
    """
    api_compuate_alpha_beta_to_csv_img(
        position_csv=result_position_path, 
        date_col=position_time_series_date_col, 
        position_col=position_time_series_position_col, 
        start_date=start_date, 
        end_date=end_date, 
        benchmark_ticker=benchmark_ticker,
        period='month',
        result_path=path_result_folder,
        norgate=norgate
    )
    print('monthly alpha beta done')
     
    """
    yearly alpha beta
    """
    api_compuate_alpha_beta_to_csv_img(
        position_csv=result_position_path, 
        date_col=position_time_series_date_col, 
        position_col=position_time_series_position_col, 
        start_date=start_date, 
        end_date=end_date, 
        benchmark_ticker=benchmark_ticker,
        period='year',
        result_path=path_result_folder,
        norgate=norgate
    )
    print('yearly alpha beta done')
    
    
    """
    trade perf, win rate, win_lose_pnl_ratio, trade count
    """
#     trades_csv = f'{PORTFOLIO_TIME_SERIES_FOLDER_COLLECTION}intermediate_per_track_trades.csv'
    output_perf_csv = f'{path_result_folder}/trade_perf.csv'
    api_trade_perf_from_trades_csv(path_trades_csv, output_perf_csv)
     
    strategy_baseball_card(
        position_perf_csv=perf_merge_output_path,
        trade_perf_csv=output_perf_csv,
        year_alpha_beta_csv=path_result_folder+'year_alpha_beta.csv',
        month_alpha_beta_csv=path_result_folder+'month_alpha_beta.csv',
        baseball_card_csv=path_result_folder+'baseball_card_strategy_perf.csv',
    )
    
    """
    OUTPUT: per year time series
    """
    input_timeseries = f'{path_result_folder}baseball_card_position_time_series.csv'
    output_folder = f'{path_result_folder}per_year_chart/'
    if not os.path.exists(output_folder):
        os.mkdir(output_folder) 
    gen_per_year_position_timeseries(
        start_date=start_date, 
        end_date=end_date, 
        col_benchmark=benchmark_ticker,
        col_portfolio='portfolio',
        col_date='date',
        output_folder=output_folder,
        input_timeseries=input_timeseries
    )
     
     
    out_path_vs_benchmark = f'{path_result_folder}'
    gen_vs_benchmark(
        timeseries_path=input_timeseries, 
        col_date='date', 
        col_benchmark=benchmark_ticker, 
        col_portfolio='portfolio', 
        out_path=out_path_vs_benchmark
    )
