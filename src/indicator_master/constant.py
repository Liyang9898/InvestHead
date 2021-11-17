'''
Created on Jun 7, 2020

@author: leon
'''

# all CSV file interface and CSV file related dataframe interface must be ONLY declared here

price_interface=['time', 'open','high','low','close','ma200','ma50','ema21','ema8']
indicator_interface = [
    # original
    'time', 
    'open',
    'high',
    'low',
    'close',
    'ma200',
    'ma50',
    'ema20',
    'ema21',
    'ema8',
    'ema55',

    # indicator
    'est_datetime',
    'date',
    'est_time',
    'sequence_8_21_50',
    'sequence_8_21',
    'sequence_p_8_21',
    'sequence_8_21_50_short',
    'sequence_8_21_50_long',
    'sequence_8_21_50_na',
    'sequence_8_21_short',
    'sequence_8_21_long',
    'sequence_8_21_na',
    'sequence_p_8_21_short',
    'sequence_p_8_21_long',
    'ema8_p_distance %',
    'ema8_v',
    'consecutive_sequence_8_21_cnt',
    'cover_lh_8',
    'cover_lh_21',
    'ema8_1day_projectile',
    'ema8_delta',
    'ema21_delta',
    'ma50_delta',
    'sequence_8_21_strict',
    'sequence_8_21_50_strict',
    'high_open_p',
    'low_open_p',
    'ema21_ma50_gap',
    'ema8_ema21_gap',
    'ema21_ma50_gap_ma',
    'ema21_ma50_MACD',
    'ema8_ema21_gap_ma',
    'ema8_ema21_MACD',
    'macd_positive',
    'macd_negative',
    
    
    # channel low
    'barlow_2_ema8',
    'barlow_2_ema8_channel_min',
    'barlow_2_ema8_channel_max',
    'barlow_2_ema8_channel_mp25_pos',
    'barlow_2_ema8_channel_mp50_pos',
    'barlow_2_ema8_channel_mp75_pos',
    'barlow_2_ema8_channel_ceiling',
    'barlow_2_ema8_channel_floor',
#     #channel high
#     'barhigh_2_ema8',
#     'barhigh_2_ema8_channel_min',
#     'barhigh_2_ema8_channel_max',
#     'barhigh_2_ema8_channel_mp25_pos',
#     'barhigh_2_ema8_channel_mp50_pos',
#     'barhigh_2_ema8_channel_mp75_pos',
#     'barhigh_2_ema8_channel_ceiling',
#     'barhigh_2_ema8_channel_floor',
#     
#     # Ribbon, ema55_20gap
#     'ema55_20_gap_delta_up',
#     'ema55_20_gap_delta_down',
#     'ema55_20_gap',
#     'ema55_20_gap_delta',
#     
#     'shrink_block',
#     'shrink_block_mark',
#     'ribbon_expand_seq',
#     'ribbon_expand_seq_1st',
#     'ribbon_expand_seq_2st',
#     'ribbon_expand_seq_3st',
#     
#     # velocity
#     'v_p_3d',
#     'v_p_1w',
#     'v_p_2w',
#     
#     # price movement
#     'delta_p_3d',
#     'delta_p_1w',
#     'delta_p_2w',
#     
#     # signal in past x days
#     'ma_upcross_in_past_3days',
#     'ma_gap_reverse_in_past_6days',
#     'ma21_local_min_in_past_6days',
#     
#     # today signal
#     'ema21_ma50_upcross',
#     'ema21_ma50_gap_local_min',
#     'ema21_local_min',
    
    # percentile
    'barlow_2_ema21_percent_oneyear_channel_percentile',
    'barlow_2_ema21_percent_oneyear_channel_100',
    'barlow_2_ema21_percent_oneyear_channel_75',
    'barlow_2_ema21_percent_oneyear_channel_50',
    'barlow_2_ema21_percent_oneyear_channel_25',
    'barlow_2_ema21_percent_oneyear_channel_0'
    
    # price velocity
#     'p_delta_oc',
#     'p_delta_1d',
#     'p_delta_2d',
#     'p_delta_3d',
#     'p_delta_5d',
#     'p_delta_10d',
#     'p_delta_20d',
#       
#     'p_delta_oc_pct',
#     'p_delta_1d_pct',
#     'p_delta_2d_pct',
#     'p_delta_3d_pct',
#     'p_delta_5d_pct',
#     'p_delta_10d_pct',
#     'p_delta_20d_pct',    
#       
#     'velocity_ui'
    
#     'enter_ui',
#     'up',
#     'down',
#     'channel_50'
]

trade_summary_interface=[
    'win_rate', 
    'lose_rate', 
    'neutral_rate', 
    'win', 
    'lose', 
    'neutral', 
    'total_trades', 
    'win_pnl_p', 
    'lose_pnl_p',
    'trading_params',
    'total_rate'
]