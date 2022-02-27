from batch_20201214.reuse_position.reuse_position_lib import merge_n_track_into_one_timeseries
from batch_20220214.batch_20220214_lib.constant import START_DATE, END_DATE, \
    PORTFOLIO_TIME_SERIES_FOLDER_SNP500
from batch_20220214.batch_20220214_lib.ui_per_track_stock_price_series import gen_per_track_st_price_pic


path = 'D:/f_data/batch_20220214/step8_portfolio_time_series/intermediate_per_track_ticker_price.csv'
folder_out = 'D:/f_data/batch_20220214/step8_portfolio_time_series/per_track_st_price/'
start_date = START_DATE
end_date = END_DATE
 
 
gen_per_track_st_price_pic(
    path,
    folder_out,
    start_date,
    end_date
)