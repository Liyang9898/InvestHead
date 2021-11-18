
from api.api import api_gen_trades
from strategy_lib.stratage_param import strat_param_20211006_ma_only_exit


indicator_file_path = 'D:/f_data/indicator_asset/20210704_swing_only/FB.csv'
trade_result_all_entry_path = 'D:/f_data/temp/trade_fb/a1.csv'
trade_result_consecutive_entry_path = 'D:/f_data/temp/trade_fb/a2.csv'
ticker = 'fb'
start_date = '2000-01-01'
end_date = '2022-01-01'
strategy = strat_param_20211006_ma_only_exit

api_gen_trades(
    ticker,
    start_date, 
    end_date, 
    strategy,
    indicator_file_path, 
    trade_result_all_entry_path, 
    trade_result_consecutive_entry_path, 
)

# api_gen_trades_summary(trade_result_all_entry_path)