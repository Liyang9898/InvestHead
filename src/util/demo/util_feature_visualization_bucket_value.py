import pandas as pd
from util.general_ui import plot_candle_stick
from util.util_feature_visualization import bucket_positive_rate
from util.util_pandas import df_general_time_filter


# extract exact sample in a bucket
bucket_path = 'D:/f_data/temp/v_to_21_50_cross_training_eval_bucketed.csv'
path = 'D:/f_data/price_with_indicator/SPY_1D_fmt_idc.csv'
df_ticker = pd.read_csv(path)
df_ticker=df_general_time_filter(df=df_ticker, date_col='est_datetime', s='2019-04-19 09:30:00', e='2021-06-19 09:30:00')

df_b = pd.read_csv(bucket_path)
feature='price_velocity_1d_pct'
df_b_select=df_b[df_b['bucket_mid']<=-0.02]
df_b_select = df_b_select[['date', 'label', 'bucket_mid' ,feature]]
# df_b_select.sort_values(by='bucket_mid', inplace=True)
print(df_b_select)


df_b_select = df_b_select[df_b_select['bucket_mid'] < -0.03]
positive = df_b_select[df_b_select['label']==True]
negative = df_b_select[df_b_select['label']==False]

date_marker = positive['date'].tolist()
date_marker2 = negative['date'].tolist()


plot_candle_stick(df_ticker, date_marker=date_marker, date_marker2=date_marker2, ticker='default')