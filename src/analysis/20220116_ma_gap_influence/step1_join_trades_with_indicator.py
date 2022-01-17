from util.util_file import get_all_csv_file_in_folder
import pandas as pd

base_folder = 'D:/f_data/batch_20211116_strat_param_swing_2150in_2150out_ma_gap_no_take_profit/'

trade_folder = base_folder + 'step3_add_indicator/'
indicator_folder = base_folder + 'step4_gen_trades/'
trade_with_idc_folder = 'D:/f_data/analysis/20220116_ma_gap_influence/'



def join_trades_with_indicator(
    trade_csv,
    indicator_csv,
    output_csv
):
    """
    given a ticker's trade and indicator, trade left join indicator on entry time
    """
    trade = pd.read_csv(trade_csv)
    indicator = pd.read_csv(indicator_csv)
    print(len(trade), len(indicator))
    # validation
    
    return


files = get_all_csv_file_in_folder(indicator_folder)

for file in files:
    if 'consecutive' in file:
        continue # only use useful
    print(file)
    
    file_name = file.split('/')[-1]
    ticker = file_name.split('_')[0]
    idc_csv = trade_folder + ticker + '.csv'
    out_csv = trade_with_idc_folder + ticker + '_trade_with_idc.csv'
    join_trades_with_indicator(
        trade_csv=file,
        indicator_csv=idc_csv,
        output_csv=out_csv
    )
