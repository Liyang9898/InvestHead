from datetime import datetime
import random

from api.api import api_download_ticker, api_position_perf_from_csv, \
    api_compuate_alpha_beta_to_csv_img, api_trade_perf_from_trades_csv
from batch_20220214.batch_20220214_lib.constant import PORTFOLIO_TIME_SERIES_FOLDER_SNP500, CONCLUSION_FOLDER, BENCHMARK_TICKER
from batch_20220214.batch_20220214_lib.stat_lib import gen_perf_stat_from_position_time_series
from batch_20220214.batch_20220214_lib.ui_multi_year_chart import gen_per_year_position_timeseries, \
    gen_vs_benchmark
from batch_20220214.batch_20220214_lib.util_batch_simulation import position_time_series_append_benchmark_to_csv_png, \
    strategy_baseball_card
import pandas as pd
import pandas as pd
from util.general_ui import plot_bars_from_xy_list, plot_points_from_xy_list


raw = 'C:/f_data/analysis/20220306_spx_alone_1970_1990/position.csv'
result_position_path = 'C:/f_data/analysis/20220306_spx_alone_1970_1990/position_fmt.csv'
df = pd.read_csv(raw)
df['date'] = pd.to_datetime(df["date"]).dt.date
df.to_csv(result_position_path)


path_position_time_series = result_position_path
position_time_series_date_col = 'date'
position_time_series_position_col = 'roll'
path_result_folder = 'C:/f_data/analysis/20220306_spx_alone_1970_1990/results/'
path_trades_csv = 'C:/f_data/analysis/20220306_spx_alone_1970_1990/SPX_1W_fmt_trades_all_consecutive_2.csv'
start_date = '1970-01-01'
end_date = '1990-01-01'
benchmark_ticker = BENCHMARK_TICKER
norgate = True


gen_perf_stat_from_position_time_series(
    path_position_time_series, # requirement
    position_time_series_date_col,
    position_time_series_position_col,
    path_trades_csv,
    path_result_folder,
    benchmark_ticker,
    start_date, # can be automated TODO
    end_date,
    norgate=True
)