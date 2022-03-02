from batch_20220214.batch_20220214_lib.constant import START_DATE, END_DATE, \
    PORTFOLIO_TIME_SERIES_FOLDER_SNP500, DEBUG_FOLDER
from batch_20220214.batch_20220214_lib.ui_per_track_stock_price_series import gen_per_track_st_price_pic


start_date = '2001-01-01'
end_date = '2002-01-01'
output_folder = PORTFOLIO_TIME_SERIES_FOLDER_SNP500
per_track_ticker_price_path = f'{output_folder}intermediate_per_track_ticker_price.csv'
folder_out = DEBUG_FOLDER


gen_per_track_st_price_pic(
    per_track_ticker_price_path,
    folder_out,
    start_date,
    end_date
)