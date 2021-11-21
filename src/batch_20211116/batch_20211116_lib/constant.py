TICKERS_RUSSLL1000_OF_ALL_TIME = 'D:/f_data/batch_20211116/step1_ticker_collection/russell1000_ticker_of_all_time.csv'
TICKERS_PRICE_FOLDER_RUSSLL1000_OF_ALL_TIME = 'D:/f_data/batch_20211116/step2_download_price_data/'
INDICATOR_FOLDER_RUSSLL1000_OF_ALL_TIME = 'D:/f_data/batch_20211116/step3_add_indicator/'
RAWS_TRADES_FOLDER_RUSSLL1000_OF_ALL_TIME = 'D:/f_data/batch_20211116/step4_gen_trades/'
TIME_RANGE_TRADES_FOLDER_RUSSLL1000_OF_ALL_TIME = 'D:/f_data/batch_20211116/step5_trade_summary_time_window/trades_time_ranged/'
TRADE_SUMMARY_PER_TICKER = 'D:/f_data/batch_20211116/step5_trade_summary_time_window/trade_summary_per_ticker/'
TRADE_SUMMARY_ALL_TICKER = 'D:/f_data/batch_20211116/step5_trade_summary_time_window/trade_summary_all_ticker/'
TICKER_RANK_FOLDER = 'D:/f_data/batch_20211116/step6_ticker_rank/'

START_DATE = '2006-01-01'
END_DATE = '2022-01-01'
START_YEAR = int(START_DATE.split('-')[0])
END_YEAR = int(END_DATE.split('-')[0])
WINDOW_SIZE = 3 # YEARS

def trade_all_entry_path(ticker):
    return f'{RAWS_TRADES_FOLDER_RUSSLL1000_OF_ALL_TIME}{ticker}_all_entry.csv'


def trade_consecutive_path(ticker):
    return f'{RAWS_TRADES_FOLDER_RUSSLL1000_OF_ALL_TIME}{ticker}_consecutive.csv'


def indicator_path(ticker):
    return f'{INDICATOR_FOLDER_RUSSLL1000_OF_ALL_TIME}{ticker}.csv'


def trade_summary_per_ticker_path(ticker,start_date,end_date):
    return f'{TRADE_SUMMARY_PER_TICKER}{ticker}_{start_date}_{end_date}.csv'


def trade_summary_all_ticker_path(start_date,end_date):
    return f'{TRADE_SUMMARY_ALL_TICKER}{start_date}_{end_date}.csv'


def ranked_ticker_path(filename):
    return f'{TICKER_RANK_FOLDER}{filename}'

def gen_time_window(window_size, start_year, end_year):
    window = []
    for start in range(start_year, end_year + 1 - window_size):
        end = start + 3
        start = str(start) + '-01-01'
        end = str(end) + '-01-01'
        window.append({'start':start, 'end':end})
    return window
    
