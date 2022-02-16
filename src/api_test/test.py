

from api.api import api_gen_trades, api_gen_trade_summary, \
    api_build_portfolio_time_series, \
    api_position_perf_from_csv, api_compuate_alpha_beta_to_csv_img, \
    api_trade_perf_from_trades_csv, api_download_ticker, api_gen_indicator, \
    api_plot_indicator_from_csv
from strategy_lib.stratage_param import strat_param_20211006_ma_only_exit
from trading_floor.api_trade.api import gen_trades_summary_from_csv, \
    gen_trades_to_csv


start_date = '2000-01-01'
end_date = '2022-01-01'
strategy = strat_param_20211006_ma_only_exit

# path
ticker = 'A-197701'
# ticker_path = 'D:/f_data/temp/trade_fb/raw.csv'
# indicator_file_path = 'D:/f_data/indicator_asset/20210704_swing_only/FB.csv'
# trade_result_all_entry_path = 'D:/f_data/temp/trade_fb/a_all.csv'
# trade_result_consecutive_entry_path = 'D:/f_data/temp/trade_fb/a_con.csv'
# trade_summary_path = 'D:/f_data/temp/trade_fb/trade_summary.csv'
# 
start_date = '1958-01-01'
end_date = '2022-01-01'
path_out_ticker_download = 'D:/f_data/temp/norgate/test.csv'
path_out_ticker_download_norgate = 'D:/f_data/temp/norgate/test_norgate.csv'
api_download_ticker(ticker, '1958-01-01', '2022-01-01', path_out_ticker_download, '1d', norgate=False)
# api_download_ticker(ticker, '2022-01-01', '2022-02-01', path_out_ticker_download_norgate, '1d', norgate=True)
# idc_not_norgate = 'D:/f_data/temp/norgate/idc_not_norgate.csv'
# idc_norgate = 'D:/f_data/temp/norgate/idc_norgate.csv'
# api_gen_indicator(path_out_ticker_download, idc_not_norgate, start_date, end_date)
# api_gen_indicator(path_out_ticker_download_norgate, idc_norgate, start_date, end_date)
# api_plot_indicator_from_csv(idc_not_norgate)
# api_plot_indicator_from_csv(idc_norgate)
# api_gen_trades(
#     ticker,
#     start_date, 
#     end_date, 
#     strategy,
#     indicator_file_path, 
#     trade_result_all_entry_path, 
#     trade_result_consecutive_entry_path, 
# )
# 
# 
# api_gen_trade_summary(
#     trade_result_all_entry_path,
#     trade_result_consecutive_entry_path,
#     trade_summary_path,
#     start_date, 
#     end_date, 
# )

# api_build_portfolio_time_series(
#     start_date=start_date,
#     end_date=end_date,
#     trade_folder="D:/f_data/batch_20211116/step7_high_perf_trades/",
#     indicator_folder="D:/f_data/batch_20211116/step3_add_indicator/",
#     output_folder='D:/f_data/temp/re/',
# )


# position_path = 'D:/f_data/batch_20211116/step8_portfolio_time_series/position.csv'
# start_date = '2009-01-01'
# end_date = '2022-01-01'
# date_col = 'date'
# position_col = 'roll'
# perf_output_path = 'D:/f_data/temp/xxxx.csv'
# 
#         
# api_position_perf_from_csv(
#     position_path, 
#     start_date, 
#     end_date, 
#     date_col, 
#     position_col,
#     perf_output_path
# )        
# 
# 
# position_csv = 'D:/f_data/batch_20211116/step8_portfolio_time_series/position.csv'
# date_col = 'date'
# position_col = 'roll'
# START_DATE = '2006-01-01'
# ANALYSIS_START_DATE = '2009-01-01' # DUE TO 3 YEARS OF HISTORICAL PERF COLLECTION 
# END_DATE = '2022-01-01'
# result_path = 'D:/f_data/temp/ab/'
# benchmark_ticker = 'SPY'
# period = 'year'
# 
# api_compuate_alpha_beta_to_csv_img(
#     position_csv, 
#     date_col, 
#     position_col, 
#     start_date, 
#     end_date, 
#     benchmark_ticker,
#     period,
#     result_path=result_path
# )

# trades_csv = 'D:/f_data/batch_20211116/step8_portfolio_time_series/intermediate_per_track_trades.csv'
# output_perf_csv = 'D:/f_data/temp/ab/trade_perf.csv'
# api_trade_perf_from_trades_csv(trades_csv, output_perf_csv)