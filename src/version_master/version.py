'''
Created on Feb 21, 2021

@author: leon
'''
from global_constant.global_constant import root_path


# feature
feature_engineering = f"{root_path}/feature_engineering/"
feature_engineering_split = f"{root_path}/feature_engineering/split/"
feature_engineering_by_ticker = f"{root_path}/feature_engineering/by_ticker/"

# indicator
indicator_20210209 = f"{root_path}/sweep_20201214/indicator/2021-02-09/"
indicator_20210226 = f"{root_path}/sweep_20201214/indicator/2021-02-26/"
indicator_20210301 = f"{root_path}/sweep_20201214/indicator/2021-03-01/"
indicator_20210404 = f"{root_path}/sweep_20201214/indicator/2021-04-04/"
indicator_20210408 = f"{root_path}/sweep_20201214/indicator/2021-04-08/"

# trades
trade_swing_smooth_prod_20210221 = f"{root_path}/sweep_20201214/trades/20210220_swing_smooth_russell1000/"
trade_swing_2150in_821out_20210226_iwf = f"{root_path}/sweep_20201214/trades/2150in_821out_20210226_iwf/"
trade_swing_2150in_850out_20210227_iwf = f"{root_path}/sweep_20201214/trades/2150in_850out_20210227_iwf/"
trade_swing_2150in_2150out_20210227_iwf = f"{root_path}/sweep_20201214/trades/2150in_2150out_20210227_iwf/"
trade_swing_2150in_2150out_20210302_iwf_trend_start = f"{root_path}/sweep_20201214/trades/2150in_2150out_20210302_iwf_trend_start/"
trade_swing_2150in_2150out_20210302_iwf_channel = f"{root_path}/sweep_20201214/trades/2150in_2150out_20210302_iwf_channel/"
trade_swing_2150in_2150out_20210310_iwf_channel_in = f"{root_path}/sweep_20201214/trades/2150in_2150out_20210310_iwf_channel_in/"
trade_swing_2150in_2150out_20210310_iwf_channel_out = f"{root_path}/sweep_20201214/trades/2150in_2150out_20210310_iwf_channel_out/"
trade_swing_2150in_2150out_20210310_iwf_channel_inout = f"{root_path}/sweep_20201214/trades/2150in_2150out_20210310_iwf_channel_inout/"

trade_swing_2150in_2150out_20210313_iwf = f"{root_path}/sweep_20201214/trades/20210313_2150in_2150out_iwf/"
trade_swing_2150in_2150out_20210313_iwf_channel_in = f"{root_path}/sweep_20201214/trades/20210313_2150in_2150out_iwf_channel_in/"

# major
trade_swing_2150in_2150out_20210313_iwf_50up = f"{root_path}/sweep_20201214/trades/20210314_iwf_ma50up/"

trade_swing_2150in_2150out_20210313_iwf_50down = f"{root_path}/sweep_20201214/trades/20210314_iwf_ma50down/"

t_20210314_iwf_ma50up_channel_out = f"{root_path}/sweep_20201214/trades/20210314_iwf_ma50up_channel_out/"
t_20210314_iwf_ma50up_channel_inout = f"{root_path}/sweep_20201214/trades/20210314_iwf_ma50up_channel_inout/"

t_20210321_myswing_20210321 =  f"{root_path}/sweep_20201214/trades/t_20210321_myswing/"

# major-2
t_20210321_myswing = f"{root_path}/sweep_20201214/trades/20210321_myswing/"
t_20210321_iwf_ma50up = f"{root_path}/sweep_20201214/trades/20210321_iwf_ma50up/"

t_20210404_myswing_4percent_out = f"{root_path}/sweep_20201214/trades/20210404_myswing_4percent_out/"
t_20210404_myswing = f"{root_path}/sweep_20201214/trades/t_20210404_myswing/"
t_20210408_myswing = f"{root_path}/sweep_20201214/trades/t_20210408_myswing/"
t_20210418_myswing = f"{root_path}/sweep_20201214/trades/t_20210418_myswing_ema21_ma50_gap/"
t_20210420_ema21_ma50_gap_per_ticker = f"{root_path}/sweep_20201214/trades/t_20210420_ema21_ma50_gap_per_ticker/"
t_20210425_ema21_ma50_gap_per_ticker_4p_out = f"{root_path}/sweep_20201214/trades/t_20210425_ema21_ma50_gap_per_ticker_4p_out/"
t_20210511_ema21_ma50_gap_per_ticker_no_profit_manage = f"{root_path}/sweep_20201214/trades/t_20210511_ema21_ma50_no_profit_manage/"
t_20210511_ema21_ma50_gap_per_ticker_3p_out = f"{root_path}/sweep_20201214/trades/t_20210511_ema21_ma50_3pout/"
# take profit experiment
t_20210518_ema21_ma50_gap_per_ticker_6p_out = f"{root_path}/sweep_20201214/trades/t_20210518_ema21_ma50_gap_per_ticker_6p_out/"
t_20210518_ema21_ma50_gap_per_ticker_8p_out = f"{root_path}/sweep_20201214/trades/t_20210518_ema21_ma50_gap_per_ticker_8p_out/"
t_20210518_ema21_ma50_gap_per_ticker_10p_out = f"{root_path}/sweep_20201214/trades/t_20210518_ema21_ma50_gap_per_ticker_10p_out/"
t_20210518_ema21_ma50_gap_per_ticker_12p_out = f"{root_path}/sweep_20201214/trades/t_20210518_ema21_ma50_gap_per_ticker_12p_out/"

# set
russell1000 = f"{root_path}/sweep_20201214/filtered/russel1000_2021jan.csv"
iwf=f"{root_path}/etf/iwf_2021_02_21.csv"
iwf_up=f"{root_path}/etf/iwf_ma50_60up_2021_02_21.csv"
iwf_down=f"{root_path}/etf/iwf_ma50_60down_2021_02_21.csv"

swing_set1=f"{root_path}/sweep_20201214/ticker_set/swing_set.csv"
swing_set_20220103 = f"{root_path}/sweep_20201214/ticker_set/russell1000_3year_historical.csv"

# experiment on iwf effect in russell1000
exp_r1000 = f"{root_path}/etf/exp_r1000.csv"
exp_iwf = f"{root_path}/etf/exp_iwf.csv"
exp_exclude_iwf = f"{root_path}/etf/exp_exclude_iwf.csv"


#trade_meta
meta_20210117 = f'{root_path}/sweep_20201214/all_ticker_meta/20210117_ticker_meta_with_vol.csv'

 
# operation data asset
op_path_base = f'{root_path}/operation/'
op_ib_report_raw = f'{root_path}/operation/ib_report_raw/'
op_ib_order_raw = f'{root_path}/operation/ib_order_raw/'
op_record = f'{root_path}/operation/record.csv'
op_close = f'{root_path}/operation/closed.csv'

# price asset
price_asset_path_base = f'{root_path}/price_asset/'

# indicator asset
indicator_asset_path_base = f'{root_path}/indicator_asset/'

# image folder
imagine_folder = f"{root_path}/image/"

# strategy param per ticker
ema21_ma50_gap_threshold = f'{root_path}/strat_param_per_ticker/ema21_ma50_per_ticker.csv'
