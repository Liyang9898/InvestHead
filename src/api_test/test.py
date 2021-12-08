

from api.api import api_gen_trades, api_gen_trade_summary, \
    api_build_portfolio_time_series, \
    api_position_perf_from_csv
from strategy_lib.stratage_param import strat_param_20211006_ma_only_exit
from trading_floor.api_trade.api import gen_trades_summary_from_csv, \
    gen_trades_to_csv


start_date = '2000-01-01'
end_date = '2022-01-01'
strategy = strat_param_20211006_ma_only_exit

# path
ticker = 'fb'
ticker_path = 'D:/f_data/temp/trade_fb/raw.csv'
indicator_file_path = 'D:/f_data/indicator_asset/20210704_swing_only/FB.csv'
trade_result_all_entry_path = 'D:/f_data/temp/trade_fb/a_all.csv'
trade_result_consecutive_entry_path = 'D:/f_data/temp/trade_fb/a_con.csv'
trade_summary_path = 'D:/f_data/temp/trade_fb/trade_summary.csv'



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


position_path = 'D:/f_data/batch_20211116/step8_portfolio_time_series/position.csv'
start_date = '2009-01-01'
end_date = '2022-01-01'
date_col = 'date'
position_col = 'roll'
perf_output_path = 'D:/f_data/temp/xxxx.csv'

        
api_position_perf_from_csv(
    position_path, 
    start_date, 
    end_date, 
    date_col, 
    position_col,
    perf_output_path
)        