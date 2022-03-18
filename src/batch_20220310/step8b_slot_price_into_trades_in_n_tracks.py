from batch_20201214.reuse_position.reuse_position_lib import slot_price_into_trades_in_n_tracks
from batch_20220310.batch_20220310_lib.constant import START_DATE, END_DATE, \
    HIGH_PERF_TRADES_FOLDER_COLLECTION_OF_ALL_TIME, \
    INDICATOR_FOLDER_COLLECTION_OF_ALL_TIME, \
    PORTFOLIO_TIME_SERIES_FOLDER_COLLECTION


"""
This process slot price into trades for N tracks
input: 
output: stock price time series in N tracks
"""
slot_price_into_trades_in_n_tracks(
    start_date=START_DATE,
    end_date=END_DATE,
    trade_folder=HIGH_PERF_TRADES_FOLDER_COLLECTION_OF_ALL_TIME,
    indicator_folder=INDICATOR_FOLDER_COLLECTION_OF_ALL_TIME,
    output_folder=PORTFOLIO_TIME_SERIES_FOLDER_COLLECTION,
    capacity=50,
)
