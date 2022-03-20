"""
This process slot best trade into N tracks
input: trades, stock pick strategy, high perf ticker in 3 year moving window
output: trades with track id in CSV
"""

from batch_20201214.reuse_position.reuse_position_lib import slot_top_trades_into_n_tracks
from batch_20220310.batch_20220310_lib.constant import START_DATE, END_DATE, \
    HIGH_PERF_TRADES_FOLDER_COLLECTION_OF_ALL_TIME, \
    PORTFOLIO_TIME_SERIES_FOLDER_COLLECTION, HIGH_PERF_TICKER_FOLDER, \
    STOCK_SELECTION_STRATEGY, PATH_TRADABLE_DAYS, PENNY_STOCK_DOLLAR_THRESHOLD


slot_top_trades_into_n_tracks(
    start_date=START_DATE,
    end_date=END_DATE,
    trade_folder=HIGH_PERF_TRADES_FOLDER_COLLECTION_OF_ALL_TIME,
    ticker_rank_folder=HIGH_PERF_TICKER_FOLDER,
    tradable_days_path=PATH_TRADABLE_DAYS,
    penny_stock_threshold=PENNY_STOCK_DOLLAR_THRESHOLD,
    output_folder=PORTFOLIO_TIME_SERIES_FOLDER_COLLECTION,
    stock_pick_strategy=STOCK_SELECTION_STRATEGY,
    capacity=50,
)
