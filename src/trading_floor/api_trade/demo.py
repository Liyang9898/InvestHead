# from api.api import api_gen_trades
from api.api import api_gen_trade_summary
from strategy_lib.stratage_param import strat_param_20211006_ma_only_exit
from trading_floor.api_trade.api import gen_trades_summary_from_csv, \
    gen_trades_to_csv


indicator_file_path = 'D:/f_data/indicator_asset/20210704_swing_only/FB.csv'
trade_result_all_entry_path = 'D:/f_data/temp/trade_fb/a_all.csv'
trade_result_consecutive_entry_path = 'D:/f_data/temp/trade_fb/a_con.csv'
trade_summary_path = 'D:/f_data/temp/trade_fb/trade_summary.csv'
ticker = 'fb'
start_date = '2000-01-01'
end_date = '2022-01-01'
strategy = strat_param_20211006_ma_only_exit


gen_trades_to_csv(
    ticker,
    start_date, 
    end_date, 
    strategy,
    indicator_file_path, 
    trade_result_all_entry_path, 
    trade_result_consecutive_entry_path, 
)


# gen_trades_summary_from_csv(
#     trade_result_all_entry_path,
#     trade_result_consecutive_entry_path,
#     trade_summary_path,
#     start_date, 
#     end_date, 
# )

api_gen_trade_summary(
    trade_result_all_entry_path,
    trade_result_consecutive_entry_path,
    trade_summary_path,
    start_date, 
    end_date, 
)