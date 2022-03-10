from batch_20220214.batch_20220214_lib.constant import START_DATE, END_DATE, \
    PORTFOLIO_TIME_SERIES_FOLDER_SNP500, DEBUG_FOLDER
from batch_20220214.batch_20220214_lib.ui_per_track_stock_price_series import gen_per_track_st_price_pic, \
    gen_per_track_position_pic


start_date = '2007-02-12'
end_date = '2008-05-12'
# start_date = '1970-01-01'
# end_date = '2023-01-01'
output_folder = PORTFOLIO_TIME_SERIES_FOLDER_SNP500
per_track_ticker_price_path = f'{output_folder}intermediate_per_track_ticker_price.csv'
per_track_ticker_position_path = f'{output_folder}intermediate_per_track_position.csv'
folder_out_price = DEBUG_FOLDER + 'price/'
folder_out_position = DEBUG_FOLDER + 'position/'


gen_per_track_st_price_pic(
    per_track_ticker_price_path,
    folder_out_price,
    start_date,
    end_date
)

gen_per_track_position_pic(
    per_track_ticker_position_path,
    folder_out_position,
    start_date,
    end_date
)