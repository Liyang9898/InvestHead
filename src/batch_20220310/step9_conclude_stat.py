from batch_20220310.batch_20220310_lib.constant import PORTFOLIO_TIME_SERIES_FOLDER_COLLECTION, \
    ANALYSIS_START_DATE, END_DATE, CONCLUSION_FOLDER, BENCHMARK_TICKER
from batch_20220310.batch_20220310_lib.stat_lib import gen_perf_stat_from_position_time_series



ANALYSIS_START_DATE = '1991-01-01'


path_position_time_series = PORTFOLIO_TIME_SERIES_FOLDER_COLLECTION + 'position.csv'
path_trades_csv = f'{PORTFOLIO_TIME_SERIES_FOLDER_COLLECTION}intermediate_per_track_trades.csv'

position_time_series_date_col = 'date'
position_time_series_position_col = 'roll'
path_result_folder = CONCLUSION_FOLDER
start_date = ANALYSIS_START_DATE
end_date = END_DATE
benchmark_ticker = BENCHMARK_TICKER
norgate = False


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