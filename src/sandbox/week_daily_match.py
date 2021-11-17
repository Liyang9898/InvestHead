import pandas as pd
from util.util_feature_visualization import chart_bucket_positive_rate, \
    chart_positive_negative_distribution, bucket_positive_rate
from util.util_time import date_to_datetime_obj, get_most_recent_monday, \
    datetime_obj_to_date_str


def entry_ts_to_monday(entry_ts):
    entry_ts_str = str(entry_ts)
    date_str = entry_ts_str.split(' ')[0]
    dt_obj = date_to_datetime_obj(date_str)
    dt_obj_mon = get_most_recent_monday(dt_obj)
    date_mon_str = get_most_recent_monday(dt_obj_mon)
    return date_mon_str

     
def add_week_mark(df):
    df['monday_week_mark'] =df.apply(lambda row : entry_ts_to_monday(row['entry_ts']), axis = 1)
    return df


def pnl_mark(pnl):
    if pnl > 0:
        return 1
    else:
        return 0
    
    
def pnl_label(pnl):
    if pnl > 0:
        return True
    else:
        return False


def add_pnl_mark(df, pnl_mark_col_name):
    df[pnl_mark_col_name] =df.apply(lambda row : pnl_mark(row['pnl']), axis = 1)
    return df

def add_pnl_label(df):
    df['pnl_label'] =df.apply(lambda row : pnl_label(row['pnl']), axis = 1)
    return df


def process_weekly(df_w):
    # add a column to mark monday of every week
    # column name 'monday_week_mark'
    df_w_marked = add_week_mark(df_w)
    return df_w_marked


def process_daily(df_d):
    # add a column to mark monday of every week
    # column name 'monday_week_mark'
    df_d_marked = add_week_mark(df_d)
    
    # if pnl > 0 then pnl_mark = 1
    df_d_marked['is_daily_trade'] = 1

    # group by 'monday_week_mark', agg pnl
    gb = df_d_marked.groupby(['monday_week_mark'])['is_daily_trade'].agg('sum')
    df_agg = pd.DataFrame(gb)
    df_agg.reset_index(inplace=True)
    
    return df_agg
    

base_path = 'D:/f_data/trades_csv/'
path_d = base_path + 'SPY_1D_fmt_trades_all_entry_2.csv'
path_w = base_path + 'SPY_1W_fmt_trades_all_entry_2.csv'

path_w_d = base_path + 'SPY_1W_1D_merge.csv'

df_d = pd.read_csv(path_d)
df_w = pd.read_csv(path_w)
# print(df_w)

df_w_processed = process_weekly(df_w)
df_d_processed = process_daily(df_d)

df_w_d = pd.merge(df_w_processed, df_d_processed, on='monday_week_mark', how='left')
df_w_d=df_w_d.fillna(0)
df_w_d=add_pnl_label(df_w_d)
df_w_d=df_w_d[['entry_ts', 'monday_week_mark', 'is_daily_trade', 'pnl_label']].copy()
# print(df_w_d.columns)
# print(df_w_d)


df_w_d.to_csv(path_w_d, index=False)

gb = df_w_d.groupby(['is_daily_trade','pnl_label']).agg('count')
gb.reset_index(inplace=True)
# print(gb)

gb_win_lose = df_w_d.groupby(['pnl_label']).agg('count')
# print(gb_win_lose)

df_w_win = df_w[df_w['pnl'] > 0]
df_w_lose = df_w[df_w['pnl'] < 0]
df_w_neu = df_w[df_w['pnl'] == 0]
print(len(df_w_win), len(df_w_lose), len(df_w_neu), len(df_w_win)/(len(df_w_win) + len(df_w_lose)))

df_d_win = df_d[df_d['pnl'] > 0]
df_d_lose = df_d[df_d['pnl'] < 0]
df_d_neu = df_d[df_d['pnl'] == 0]
print(len(df_d_win), len(df_d_lose), len(df_d_neu), len(df_d_win)/(len(df_d_win) + len(df_d_lose)))


# path = 'D:/f_data/temp/v_to_21_50_cross_training_eval.csv'
df = df_w_d # feature table
print(df.columns)
print(df)
feature='is_daily_trade'
# feature = 'price_delta_oc_pct'
label='pnl_label'
bins = 6

bucket_path = 'D:/f_data/temp/x2.csv'
ratio = bucket_positive_rate(df, feature,label, bins, bucket_path)
print(ratio)

chart_bucket_positive_rate(
    df=df, 
    feature=feature, 
    label=label, 
    bins=bins, 
)
  
chart_positive_negative_distribution(
    df=df, 
    feature=feature, 
    label=label, 
    bins=bins, 
)
 

