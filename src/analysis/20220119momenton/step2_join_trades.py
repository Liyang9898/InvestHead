from util.util_file import get_all_csv_file_in_folder
import pandas as pd

base_folder = 'D:/f_data/batch_20211116_strat_param_swing_2150in_2150out_ma_gap_4p_profit/'

trade_folder = base_folder + 'step3_add_indicator/'
indicator_folder = base_folder + 'step4_gen_trades/'
trade_with_idc_folder = 'D:/f_data/analysis/20220116_ma_gap_influence/trade_with_idc/'
sub_trades_path = 'D:/f_data/analysis/20220116_ma_gap_influence/trades_split/'


def get_date_from_entry_ts(entry_ts):
    date = entry_ts.split(' ')[0]
    return date


def join_indicator_with_trades_20220119(
    trade_csv,
    indicator_csv,
    output_csv
):
    """
    given a ticker's trade and indicator, trade left join indicator on entry time
    """
    trade = pd.read_csv(trade_csv)
    indicator = pd.read_csv(indicator_csv)
    
    # no trades
    if len(trade) == 0:
        return
    
    trade['entry_date']=trade.apply(lambda row : get_date_from_entry_ts(row['entry_ts']), axis = 1)
    trade['exit_date']=trade.apply(lambda row : get_date_from_entry_ts(row['exit_ts']), axis = 1)
     
    out = indicator.merge(trade, how='left', left_on='next_bar_date', right_on='entry_date')   # idc'date'

    # validation
    assert len(out) == len(indicator)
    out.to_csv(output_csv, index=False)


files = get_all_csv_file_in_folder('D:/f_data/analysis/20220119_momenton/idc_with_feature/')

for file in files:

 
    file_name = file.split('/')[-1]
    ticker = file_name.split('.')[0]
    print(ticker)
    
    trade_path = f'D:/f_data/batch_20211116_strat_param_swing_2150in_2150out_ma_gap_4p_profit/step4_gen_trades/{ticker}_all_entry.csv'
    print(trade_path)

    out_csv = f'D:/f_data/analysis/20220119_momenton/step2_join_trades/{ticker}.csv'
    join_indicator_with_trades_20220119(
        trade_csv=trade_path,
        indicator_csv=file,
        output_csv=out_csv
    )
