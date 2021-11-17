
folder_path_raw_downloaded = "D:/f_data/raw_downloaded_file/"
folder_path_raw_price_formated = "D:/f_data/formatted_price_file/"
folder_path_price_with_indicator = "D:/f_data/price_with_indicator/"
folder_path_trades_csv = "D:/f_data/trades_csv/"
folder_path_trade_ml_sample = "D:/f_data/trade_ml_sample/"
folder_path_trade_summary = "D:/f_data/trade_summary/"
file_type_postfix="csv"

#file naming rule
#formatted: {ticker}_{period}_fmt
#with indicator: {ticker}_{period}_fmt_idc

trade_feature = [
	'label',
	'ema_8_v_yesterday',
	'ema_21_v_yesterday',
	'ema_8_21_gap_yesterday',
	'ema_8_strict_sequence_yesterday',
	'pnl_p_per_trade',
	'entry_time',
]
