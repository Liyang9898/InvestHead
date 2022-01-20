from indicator_master.plot_indicator_lib import plot_indicator
import pandas as pd
from util.general_ui import plot_candle_stick
from util.util_time import date_add_days, df_filter_dy_date
from util.util_feature_visualization import chart_bucket_positive_rate


feature_label_merge_less4p_lose = 'D:/f_data/analysis/20220116_ma_gap_influence/feature_label_merge_less4p_lose.csv'
flat_only = 'D:/f_data/analysis/20220116_ma_gap_influence/conclusion/less4p_lose_only2.csv'
flat_only_df = pd.read_csv(flat_only)
tickers = pd.read_csv(feature_label_merge_less4p_lose)
flat_only_df=flat_only_df[~flat_only_df['flat'].isnull()]
flat_idx = flat_only_df['Unnamed: 0'].to_list()
print(flat_idx)   

  
base_folder = 'D:/f_data/batch_20211116_strat_param_swing_2150in_2150out_ma_gap_4p_profit/'
trade_folder = base_folder + 'step3_add_indicator/'
  
  
def plot_indicator_add_point(indicator_path, date1, date2, range_days, ticker, path):
    half_range = int(range_days/2)
    start_date = date_add_days(date1, -half_range)
    end_date = date_add_days(date1, half_range)
      
    df = pd.read_csv(indicator_path)
    df = df_filter_dy_date(df,'date',start_date,end_date)
#     print(start_date, end_date)
    plot_candle_stick(df, date_marker=[date1], date_marker2=[date2], ticker=ticker, path=path)
  
  
start = 0
offset = 500
  
for i in range(0, len(tickers)):
#     if not (i >= start and i < start+offset):
#         continue
    if i not in flat_idx:
        continue
    ticker = tickers.loc[i, 'ticker']
    print(i, ticker)
    s = tickers.loc[i, 'entry_date']
    e = tickers.loc[i, 'exit_date']
    indicator_path = trade_folder + ticker + '.csv'
    img_path = 'D:/f_data/analysis/20220116_ma_gap_influence/lose_picture/flat_only/' + str(i)+'_'+ticker + '.jpeg'
    plot_indicator_add_point(indicator_path, s, e, 90, str(i)+'_'+ticker, img_path)

