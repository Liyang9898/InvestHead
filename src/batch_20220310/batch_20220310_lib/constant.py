from batch_20201214.reuse_position.lib.trade_opportunity_ranking import METHOD_RANDOM, \
    METHOD_TOP_RETURN, METHOD_TOP_WIN_RATE, METHOD_TOP_WIN_LOSE_PNL_RATIO
from global_constant.global_constant import root_path


PENNY_STOCK_DOLLAR_THRESHOLD = 10
BATCH_FOLDER_NAME = 'batch_20220310'

PATH_PREPARE = f'{root_path}/{BATCH_FOLDER_NAME}/step0_prepare/'
TICKERS_COLLECTION_OF_ALL_TIME = f'{root_path}/{BATCH_FOLDER_NAME}/step1_ticker_collection/collection_ticker_of_all_time.csv'
TICKERS_PRICE_FOLDER_COLLECTION_OF_ALL_TIME = f'{root_path}/{BATCH_FOLDER_NAME}/step2_download_price_data/'
INDICATOR_FOLDER_COLLECTION_OF_ALL_TIME = f'{root_path}/{BATCH_FOLDER_NAME}/step3_add_indicator/'
RAWS_TRADES_FOLDER_COLLECTION_OF_ALL_TIME = f'{root_path}/{BATCH_FOLDER_NAME}/step4_gen_trades/'
FEATURE_THRESHOLD_FOLDER_COLLECTION_OF_ALL_TIME = f'{root_path}/{BATCH_FOLDER_NAME}/step4c_threshold/'
IDC_TRADE_THRESHOLD_FOLDER_COLLECTION_OF_ALL_TIME = f'{root_path}/{BATCH_FOLDER_NAME}/step4b_idc_trade/'

BASE_PATH = f'{root_path}/{BATCH_FOLDER_NAME}/'

HIGH_PERF_TRADES_FOLDER_COLLECTION_OF_ALL_TIME = f'{root_path}/{BATCH_FOLDER_NAME}/step7_high_perf_trades/'
TIME_RANGE_TRADES_FOLDER_COLLECTION_OF_ALL_TIME = f'{root_path}/{BATCH_FOLDER_NAME}/step5_trade_summary_time_window/trades_time_ranged/'
PORTFOLIO_TIME_SERIES_FOLDER_COLLECTION = f'{root_path}/{BATCH_FOLDER_NAME}/step8_portfolio_time_series/'
TRADE_SUMMARY_PER_TICKER = f'{root_path}/{BATCH_FOLDER_NAME}/step5_trade_summary_time_window/trade_summary_per_ticker/'
TRADE_SUMMARY_ALL_TICKER = f'{root_path}/{BATCH_FOLDER_NAME}/step5_trade_summary_time_window/trade_summary_all_ticker/'
HIGH_PERF_TICKER_FOLDER = f'{root_path}/{BATCH_FOLDER_NAME}/step6_ticker_rank/'
CONCLUSION_FOLDER = f'{root_path}/{BATCH_FOLDER_NAME}/step9_conclusion/'
DEBUG_FOLDER = f'{root_path}/{BATCH_FOLDER_NAME}/step999_optional_debug/'

"""
this section defines tradable days
"""
PATH_TRADABLE_DAYS = f'{PATH_PREPARE}tradable_days.csv'
path_spx_open_position_csv = f'{root_path}/analysis/20220307_spx_1970_2022/SPX_1W_fmt_trades_all_consecutive_2.csv'
use_trade_position_open_days = True


START_DATE = '1970-01-01'
ANALYSIS_START_DATE = '1973-01-01' # DUE TO 3 YEARS OF HISTORICAL PERF COLLECTION 
END_DATE = '2022-01-01'


# START_DATE = '1988-01-01'
# ANALYSIS_START_DATE = '1991-01-01' # DUE TO 3 YEARS OF HISTORICAL PERF COLLECTION 
# END_DATE = '2023-01-01'


START_YEAR = int(START_DATE.split('-')[0])
END_YEAR = int(END_DATE.split('-')[0])
WINDOW_SIZE = 3 # YEARS
BENCHMARK_TICKER = '$SPX'
# BENCHMARK_TICKER = '$RUI'


# STOCK_SELECTION_STRATEGY = METHOD_RANDOM
# STOCK_SELECTION_STRATEGY = METHOD_TOP_RETURN
# STOCK_SELECTION_STRATEGY = METHOD_TOP_WIN_RATE
STOCK_SELECTION_STRATEGY = METHOD_TOP_WIN_LOSE_PNL_RATIO


def trade_all_entry_path(ticker):
    return f'{RAWS_TRADES_FOLDER_COLLECTION_OF_ALL_TIME}{ticker}_all_entry.csv'


def trade_consecutive_path(ticker):
    return f'{RAWS_TRADES_FOLDER_COLLECTION_OF_ALL_TIME}{ticker}_consecutive.csv'


def indicator_path(ticker):
    return f'{INDICATOR_FOLDER_COLLECTION_OF_ALL_TIME}{ticker}.csv'


def trade_summary_per_ticker_path(ticker,start_date,end_date):
    return f'{TRADE_SUMMARY_PER_TICKER}{ticker}_{start_date}_{end_date}.csv'


def trade_summary_all_ticker_path(start_date,end_date):
    return f'{TRADE_SUMMARY_ALL_TICKER}{start_date}_{end_date}.csv'


def ranked_ticker_path(filename):
    return f'{HIGH_PERF_TICKER_FOLDER}{filename}'

def gen_time_window(window_size, start_year, end_year):
    window = []
    for start in range(start_year, end_year + 1 - window_size):
        end = start + 3
        start = str(start) + '-01-01'
        end = str(end) + '-01-01'
        window.append({'start':start, 'end':end})
    return window
    
