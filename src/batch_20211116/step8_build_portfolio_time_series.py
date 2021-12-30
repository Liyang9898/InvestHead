from api.api import api_build_portfolio_time_series
from batch_20211116.batch_20211116_lib.constant import START_DATE, END_DATE, \
    HIGH_PERF_TRADES_FOLDER_RUSSLL1000_OF_ALL_TIME, \
    INDICATOR_FOLDER_RUSSLL1000_OF_ALL_TIME, \
    PORTFOLIO_TIME_SERIES_FOLDER_RUSSLL1000, TICKER_RANK_FOLDER


api_build_portfolio_time_series(
    start_date=START_DATE,
    end_date=END_DATE,
    trade_folder=HIGH_PERF_TRADES_FOLDER_RUSSLL1000_OF_ALL_TIME,
    ticker_rank_folder=TICKER_RANK_FOLDER,
    indicator_folder=INDICATOR_FOLDER_RUSSLL1000_OF_ALL_TIME,
    output_folder=PORTFOLIO_TIME_SERIES_FOLDER_RUSSLL1000,
)
