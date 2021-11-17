'''
Created on Feb 21, 2021

@author: leon
'''
# feature
feature_engineering = "D:/f_data/feature_engineering/"
feature_engineering_split = "D:/f_data/feature_engineering/split/"
feature_engineering_by_ticker = "D:/f_data/feature_engineering/by_ticker/"

# indicator
indicator_20210209 = "D:/f_data/sweep_20201214/indicator/2021-02-09/"
indicator_20210226 = "D:/f_data/sweep_20201214/indicator/2021-02-26/"
indicator_20210301 = "D:/f_data/sweep_20201214/indicator/2021-03-01/"
indicator_20210404 = "D:/f_data/sweep_20201214/indicator/2021-04-04/"
indicator_20210408 = "D:/f_data/sweep_20201214/indicator/2021-04-08/"

# trades
trade_swing_smooth_prod_20210221 = "D:/f_data/sweep_20201214/trades/20210220_swing_smooth_russell1000/"
trade_swing_2150in_821out_20210226_iwf = "D:/f_data/sweep_20201214/trades/2150in_821out_20210226_iwf/"
trade_swing_2150in_850out_20210227_iwf = "D:/f_data/sweep_20201214/trades/2150in_850out_20210227_iwf/"
trade_swing_2150in_2150out_20210227_iwf = "D:/f_data/sweep_20201214/trades/2150in_2150out_20210227_iwf/"
trade_swing_2150in_2150out_20210302_iwf_trend_start = "D:/f_data/sweep_20201214/trades/2150in_2150out_20210302_iwf_trend_start/"
trade_swing_2150in_2150out_20210302_iwf_channel = "D:/f_data/sweep_20201214/trades/2150in_2150out_20210302_iwf_channel/"
trade_swing_2150in_2150out_20210310_iwf_channel_in = "D:/f_data/sweep_20201214/trades/2150in_2150out_20210310_iwf_channel_in/"
trade_swing_2150in_2150out_20210310_iwf_channel_out = "D:/f_data/sweep_20201214/trades/2150in_2150out_20210310_iwf_channel_out/"
trade_swing_2150in_2150out_20210310_iwf_channel_inout = "D:/f_data/sweep_20201214/trades/2150in_2150out_20210310_iwf_channel_inout/"

trade_swing_2150in_2150out_20210313_iwf = "D:/f_data/sweep_20201214/trades/20210313_2150in_2150out_iwf/"
trade_swing_2150in_2150out_20210313_iwf_channel_in = "D:/f_data/sweep_20201214/trades/20210313_2150in_2150out_iwf_channel_in/"

# major
trade_swing_2150in_2150out_20210313_iwf_50up = "D:/f_data/sweep_20201214/trades/20210314_iwf_ma50up/"

trade_swing_2150in_2150out_20210313_iwf_50down = "D:/f_data/sweep_20201214/trades/20210314_iwf_ma50down/"

t_20210314_iwf_ma50up_channel_out = "D:/f_data/sweep_20201214/trades/20210314_iwf_ma50up_channel_out/"
t_20210314_iwf_ma50up_channel_inout = "D:/f_data/sweep_20201214/trades/20210314_iwf_ma50up_channel_inout/"

t_20210321_myswing_20210321 =  "D:/f_data/sweep_20201214/trades/t_20210321_myswing/"

# major-2
t_20210321_myswing = "D:/f_data/sweep_20201214/trades/20210321_myswing/"
t_20210321_iwf_ma50up = "D:/f_data/sweep_20201214/trades/20210321_iwf_ma50up/"

t_20210404_myswing_4percent_out = "D:/f_data/sweep_20201214/trades/20210404_myswing_4percent_out/"
t_20210404_myswing = "D:/f_data/sweep_20201214/trades/t_20210404_myswing/"
t_20210408_myswing = "D:/f_data/sweep_20201214/trades/t_20210408_myswing/"
t_20210418_myswing = "D:/f_data/sweep_20201214/trades/t_20210418_myswing_ema21_ma50_gap/"
t_20210420_ema21_ma50_gap_per_ticker = "D:/f_data/sweep_20201214/trades/t_20210420_ema21_ma50_gap_per_ticker/"
t_20210425_ema21_ma50_gap_per_ticker_4p_out = "D:/f_data/sweep_20201214/trades/t_20210425_ema21_ma50_gap_per_ticker_4p_out/"
t_20210511_ema21_ma50_gap_per_ticker_no_profit_manage = "D:/f_data/sweep_20201214/trades/t_20210511_ema21_ma50_no_profit_manage/"
t_20210511_ema21_ma50_gap_per_ticker_3p_out = "D:/f_data/sweep_20201214/trades/t_20210511_ema21_ma50_3pout/"
# take profit experiment
t_20210518_ema21_ma50_gap_per_ticker_6p_out = "D:/f_data/sweep_20201214/trades/t_20210518_ema21_ma50_gap_per_ticker_6p_out/"
t_20210518_ema21_ma50_gap_per_ticker_8p_out = "D:/f_data/sweep_20201214/trades/t_20210518_ema21_ma50_gap_per_ticker_8p_out/"
t_20210518_ema21_ma50_gap_per_ticker_10p_out = "D:/f_data/sweep_20201214/trades/t_20210518_ema21_ma50_gap_per_ticker_10p_out/"
t_20210518_ema21_ma50_gap_per_ticker_12p_out = "D:/f_data/sweep_20201214/trades/t_20210518_ema21_ma50_gap_per_ticker_12p_out/"

# set
russell1000 = "D:/f_data/sweep_20201214/filtered/russel1000_2021jan.csv"
iwf="D:/f_data/etf/iwf_2021_02_21.csv"
iwf_up="D:/f_data/etf/iwf_ma50_60up_2021_02_21.csv"
iwf_down="D:/f_data/etf/iwf_ma50_60down_2021_02_21.csv"

swing_set1="D:/f_data/sweep_20201214/ticker_set/swing_set.csv"


# experiment on iwf effect in russell1000
exp_r1000 = "D:/f_data/etf/exp_r1000.csv"
exp_iwf = "D:/f_data/etf/exp_iwf.csv"
exp_exclude_iwf = "D:/f_data/etf/exp_exclude_iwf.csv"


#trade_meta
meta_20210117 = 'D:/f_data/sweep_20201214/all_ticker_meta/20210117_ticker_meta_with_vol.csv'

 
# operation data asset
op_path_base = 'D:/f_data/operation/'
op_ib_report_raw = 'D:/f_data/operation/ib_report_raw/'
op_ib_order_raw = 'D:/f_data/operation/ib_order_raw/'
op_record = 'D:/f_data/operation/record.csv'
op_close = 'D:/f_data/operation/closed.csv'

# price asset
price_asset_path_base = 'D:/f_data/price_asset/'

# indicator asset
indicator_asset_path_base = 'D:/f_data/indicator_asset/'

# image folder
imagine_folder = "D:/f_data/image/"

# strategy param per ticker
ema21_ma50_gap_threshold = 'D:/f_data/strat_param_per_ticker/ema21_ma50_per_ticker.csv'
