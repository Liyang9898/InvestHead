from indicator_master.feature_lib.date_feature import next_bar_date
from util.util_feature_visualization import get_df_feature_cumulative_cnt_win_rate


def get_date_from_entry_ts(entry_ts):
    date = entry_ts.split(' ')[0]
    return date


def label_on_pnl(pnl_percent):
    if pnl_percent > 0:
        return True
    else:
        return False


def compute_v_threshold_on_idc_trade_merged_data(df_merge, ticker):
    feature = 'v_ema21_3'
    label = 'label'
 
    df_f_gp = get_df_feature_cumulative_cnt_win_rate(df=df_merge, feature=feature, label=label)
    if df_f_gp is None:
        return
    x = df_f_gp['cnt_all_pct_big_eq_feature'].to_list()
    y = df_f_gp['win_rate_big_eq_feature'].to_list()
    win_rate_sample_cnt = dict(zip(x, y))
     
    cur_threshold = 90
    thresholds = {}
    thresholds['ticker'] = ticker
    for x in win_rate_sample_cnt.keys():
        if x < cur_threshold / 100:
            thresholds[cur_threshold] = win_rate_sample_cnt[x]
            cur_threshold = cur_threshold - 10
            if cur_threshold < 50:
                break
    
    return thresholds


def merge_idc_trade_add_label(df_idc, df_trade):
    """
    input: indicator df, trades df (both df are not empty)
    output: merger indicator and trades on dates(shift by 1), add label ->df
    """
    
    df_trade['entry_date']=df_trade.apply(lambda row : get_date_from_entry_ts(row['entry_ts']), axis = 1)
    next_bar_date(df_idc, date_col='date', feature_col='next_bar_date')
    df_merge = df_trade.merge(df_idc, how='left', left_on='entry_date', right_on='next_bar_date')   # idc'date'
    assert len(df_merge) == len(df_trade)
    df_merge['label']=df_merge.apply(lambda row : label_on_pnl(row['pnl_percent']), axis = 1)
    return df_merge