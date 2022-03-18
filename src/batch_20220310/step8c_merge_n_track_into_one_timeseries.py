from batch_20201214.reuse_position.reuse_position_lib import merge_n_track_into_one_timeseries
from batch_20220310.batch_20220310_lib.constant import START_DATE, END_DATE, \
    PORTFOLIO_TIME_SERIES_FOLDER_COLLECTION


"""
This process merge all track time series into one
input: 
output: 
"""
merge_n_track_into_one_timeseries(
    start_date=START_DATE,
    end_date=END_DATE,
    output_folder=PORTFOLIO_TIME_SERIES_FOLDER_COLLECTION,
    capacity=50,
)

