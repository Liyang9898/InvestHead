from plotly.subplots import make_subplots

import pandas as pd
import plotly.graph_objects as go
from util.general_ui import plot_lines_from_xy_list


BIG_EQ_FEATURE = 'big_eq_feature'
SMALL_EQ_FEATURE = 'small_eq_feature'


def chart_bucket_positive_rate(df, feature, label, bins, img_path=''):
    bucket = bucket_positive_rate(df, feature, label, bins)
#     print(bucket.columns)
    print(bucket)
    bucket['total'] = bucket['positive'] + bucket['negative']
    bucket['rate'] = bucket['positive'] / bucket['total']
#     print(bucket[['bucket','total','rate']])
    fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=bucket['mid'], 
            y=bucket['positive_ratio'],
            mode='lines+markers',
            name='positive_ratio'
        ),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(
            x=bucket['mid'], 
            y=bucket['sum'],
            mode='lines+markers',
            name='sample_cnt'
        ),
        secondary_y=True,
    )

    title = f'Feature positive label ratio: {feature}'
    fig.update_yaxes(title_text="Positive ratio", secondary_y=False)
    fig.update_yaxes(title_text="Distribution", secondary_y=True)
    fig.update_layout(
        title=title,
        xaxis_title_text='Feature value', # x axis label
    )

    if img_path=='':
        fig.show()
    else:
        fig.write_image(img_path)


def chart_positive_negative_distribution(df, feature, label, bins, img_path=''):
    p = df[df[label]==True]
    n = df[df[label]==False]
    
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(x=p[feature],name=f'positive: {len(p)}',nbinsx=bins,histnorm='percent'))
    fig.add_trace(go.Histogram(x=n[feature],name=f'negative: {len(n)}',nbinsx=bins,histnorm='percent'))
    
    title = f'Feature distribution: {feature}'
    fig.update_layout(
        barmode='overlay',
        title=title,
        xaxis_title_text='Feature value', # x axis label
        yaxis_title_text='Distribution', # y axis label
    )

    fig.update_traces(opacity=0.75)
    if img_path=='':
        fig.show()
    else:
        fig.write_image(img_path)
    

def bucket_positive_rate(df, feature, label, bins, bucket_path=None):
    # get bucket
    df["bucket"] = pd.cut(df[feature], bins)
    # optional save
    if bucket_path is not None:
        df['bucket_left'] = df.apply(lambda row : row['bucket'].left, axis = 1)
        df['bucket_right'] = df.apply(lambda row : row['bucket'].right, axis = 1)
        df['bucket_mid'] = df.apply(lambda row : (row['bucket'].left+row['bucket'].right)/2, axis = 1)
        df.to_csv(bucket_path, index=False)
    df.dropna(subset=['bucket'], inplace=True)
    
    # join
    cnt = df[["bucket",label,feature]].groupby(by=["bucket", label]).count()
    df_cnt = pd.DataFrame(cnt)
    df_cnt.reset_index(inplace=True)
    df_cnt_p = df_cnt[df_cnt[label]==True][['bucket',feature]]
    df_cnt_n = df_cnt[df_cnt[label]==False][['bucket',feature]]
    
    df_p = df_cnt_p.rename(columns={feature: "positive"})
    df_n = df_cnt_n.rename(columns={feature: "negative"})
    ratio = df_p.merge(df_n, how='inner', on='bucket')

    # calculate boundary
    ratio['left'] = ratio.apply(lambda row : row['bucket'].left, axis = 1)
    ratio['right'] = ratio.apply(lambda row : row['bucket'].right, axis = 1)
    ratio['mid'] = ratio.apply(lambda row : (row['bucket'].left+row['bucket'].right)/2, axis = 1)
    
    # ratio
    ratio['sum'] = ratio['positive'] + ratio['negative']
    ratio['positive_ratio'] = ratio['positive'] / ratio['sum']
    sum_sum = ratio['sum'].sum()
    ratio['distribution'] = ratio['sum'] / sum_sum
    
    # distribution_agg
    ratio['distribution_agg'] = ratio['distribution']
    for i in range(1, len(ratio)):
        ratio.loc[i, 'distribution_agg'] = ratio.loc[i-1, 'distribution_agg'] + ratio.loc[i, 'distribution']
    
    return ratio


def get_feature_label_groupby_sample_cnt(df, feature, label):
    """
    
    output: sample cnt of each feature and label group by column
    """
    gp_df = df.groupby([feature, label]).size().to_frame('cnt')
    gp_df.reset_index(inplace=True)
    
    gp_df_p = gp_df[gp_df[label] == True][[feature, 'cnt']].copy()
    gp_df_p.rename(columns={"cnt": "cnt_p"}, inplace=True)
    
    gp_df_n = gp_df[gp_df[label] == False][[feature, 'cnt']].copy()
    gp_df_n.rename(columns={"cnt": "cnt_n"}, inplace=True)
    
    df_f_gp = pd.merge(gp_df_p,gp_df_n,on=feature,how='outer')
    df_f_gp.fillna(0, inplace=True)
    
    # validation
    assert len(df) == df_f_gp['cnt_p'].sum() + df_f_gp['cnt_n'].sum()

    return df_f_gp


def get_df_feature_cumulative_cnt_win_rate(df, feature, label):
    """
    input: label must be boolean
    """  
    total_sample = len(df)
    
    # pre-process feature value group by
    df_f_gp = get_feature_label_groupby_sample_cnt(df, feature, label)
    print(df_f_gp)
    # aggregation of sample count big_eq_feature
    df_f_gp.sort_values(by=feature, inplace=True, ascending=False)
    df_f_gp.reset_index(inplace=True, drop=True)
    df_f_gp['cnt_p_big_eq_feature'] = df_f_gp['cnt_p'].cumsum()
    df_f_gp['cnt_n_big_eq_feature'] = df_f_gp['cnt_n'].cumsum()
    df_f_gp['cnt_all_big_eq_feature'] = df_f_gp['cnt_p_big_eq_feature'] + df_f_gp['cnt_n_big_eq_feature']
    df_f_gp['win_rate_big_eq_feature'] = df_f_gp['cnt_p_big_eq_feature'] / df_f_gp['cnt_all_big_eq_feature']
    df_f_gp['cnt_all_pct_big_eq_feature'] = df_f_gp['cnt_all_big_eq_feature'] / total_sample
    assert df_f_gp.loc[len(df_f_gp) - 1, 'cnt_all_big_eq_feature'] == total_sample # validation
    
    # aggregation of sample count small_eq_feature
    df_f_gp.sort_values(by=feature, inplace=True, ascending=True)
    df_f_gp.reset_index(inplace=True, drop=True)
    df_f_gp['cnt_p_small_eq_feature'] = df_f_gp['cnt_p'].cumsum()
    df_f_gp['cnt_n_small_eq_feature'] = df_f_gp['cnt_n'].cumsum()
    df_f_gp['cnt_all_small_eq_feature'] = df_f_gp['cnt_p_small_eq_feature'] + df_f_gp['cnt_n_small_eq_feature']
    df_f_gp['win_rate_small_eq_feature'] = df_f_gp['cnt_p_small_eq_feature'] / df_f_gp['cnt_all_small_eq_feature']
    df_f_gp['cnt_all_pct_small_eq_feature'] = df_f_gp['cnt_all_small_eq_feature'] / total_sample
    assert df_f_gp.loc[len(df_f_gp) - 1, 'cnt_all_small_eq_feature'] == total_sample # validation
    
    return df_f_gp


def chart_feature_cumulative_win_rate_sample_cnt(df, feature, label, direction_flag, path=None):
    """
    input: direction_flag is constant, see above
    output: chart, x is feature y is cumulative win rate and sample cnt based on direction
    """
    df_f_gp = get_df_feature_cumulative_cnt_win_rate(df, feature, label)
    total = df_f_gp['cnt_p'].sum() + df_f_gp['cnt_n'].sum()
    win_rate_avg = round(df_f_gp['cnt_p'].sum() / total, 4)
    
    x_list = df_f_gp[feature].to_list()
    y_list_map = {}
    
    if direction_flag == BIG_EQ_FEATURE:
        y_list_map = {
            'sample count-big_eq_feature': df_f_gp['cnt_all_pct_big_eq_feature'].to_list(),
            'win rate-big_eq_feature':df_f_gp['win_rate_big_eq_feature'].to_list()
        }
    elif direction_flag == SMALL_EQ_FEATURE:
        y_list_map = {
            'sample count-small_eq_feature': df_f_gp['cnt_all_pct_small_eq_feature'].to_list(),
            'win rate-small_eq_feature':df_f_gp['win_rate_small_eq_feature'].to_list()
        }
        
    title = f'y=cumulative win rate & sample count | x={feature} | flag={direction_flag} | avg_win_rate={win_rate_avg}'
    plot_lines_from_xy_list(x_list, y_list_map, title=title, path=path)  
        
    ### percent
    x_list_sample = []
    y_list_map = {}
    title = f'y=cumulative win rate | x=sample count | flag={direction_flag} | avg_win_rate={win_rate_avg}'
    if direction_flag == BIG_EQ_FEATURE:
        x_list_sample = df_f_gp['cnt_all_pct_big_eq_feature'].to_list()
        y_list_map = {
            'win rate-big_eq_feature':df_f_gp['win_rate_big_eq_feature'].to_list()
        }
        plot_lines_from_xy_list(x_list=x_list_sample, y_list_map=y_list_map, title=title, path=None)  
    elif direction_flag == SMALL_EQ_FEATURE:
        x_list_sample = df_f_gp['cnt_all_pct_small_eq_feature'].to_list()
        y_list_map = {
            'win rate-small_eq_feature':df_f_gp['win_rate_small_eq_feature'].to_list()
        }
        plot_lines_from_xy_list(x_list=x_list_sample, y_list_map=y_list_map, title=title, path=None)  
    