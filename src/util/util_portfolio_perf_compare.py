import os

from batch_20201214.download_stock.download_stock_lib import download_format_2csv
import pandas as pd
from util.util import str_to_txt, gen_random_str
from util.util_finance import  get_position_perf, compute_alpha_beta_from_position, get_line_speed_chart
from util.util_finance_chart import get_drop_chart, get_return_chart_period, \
    plot_chart_normalized_on_start, plot_chart_normalized_on_abs_return, \
    plot_chart_from_df, get_return_chart_delta_period
from util.util_pandas import df_normalize
from util.util_time import df_filter_dy_date, unixtime_to_date


# from sandbox.yahoo_st_to_perf_readable_csv import df_base
# from util.general_ui import plot_lines_from_xy_list
def perf_compare_df_pre_requisite(df, start_date, end_date):
    # validation
    print(df.columns)
    assert len(df.columns) == 3
    
    assert 'date' in df.columns
    assert 'baseline' in df.columns
    assert 'experiment' in df.columns
    assert not df.isnull().values.any()

    # filter by date
    df = df_filter_dy_date(df,'date',start_date, end_date)
    
    # sort by date, clean up
    df.sort_values(by=['date'], inplace=True)
    df.reset_index(inplace=True, drop=True)


def perf_compare(df, start_date, end_date, path=None):
    df = df.copy()
    perf_compare_df_pre_requisite(df, start_date, end_date)
 
    
    df_normalize(df=df, normalize_col='baseline')
    df_normalize(df=df, normalize_col='experiment')
      
    info_base = get_position_perf(df, 'date', 'baseline')
    info_exp = get_position_perf(df, 'date', 'experiment')
       
    # alpha beta
    info_alpha_beta = {}
    for period in ['year', 'month', 'week']:
        info_alpha_beta[period] = compute_alpha_beta_from_position(
            df=df, date_col='date', base_col='baseline', exp_col='experiment', period=period, plot=False
        )

    perf_res = {
        'baseline_perf':info_base,
        'experiment_perf':info_exp,
        'alpha_beta':info_alpha_beta,
    }
    perf_res_str = gen_perf_compare_readable_format(perf_res)
    if path is not None:
        str_to_txt(perf_res_str, path)        
    return perf_res_str


def plot_perf_compare_chart(df, start_date, end_date, path=None):
    df = df.copy()
    perf_compare_df_pre_requisite(df, start_date, end_date)
    
    print('plotting normalized chart...')
    plot_chart_normalized_on_start(df, 'date', 'baseline', 'experiment', path)
    plot_chart_normalized_on_abs_return(df, 'date', 'baseline', 'experiment', path)
    print('plotting drop chart...')
    get_drop_chart(df=df, date_col='date', base_col='baseline', exp_col='experiment', path=path)
    print('plotting speed chart...')
    get_line_speed_chart(df=df, date_col='date', baseline_col='baseline', position_col='experiment', time_bucket=1, path=path)
    print('plotting return chart...')
    get_return_chart_period(df=df, date_col='date', base_col='baseline', exp_col='experiment', period='year', path=path)
    get_return_chart_delta_period(df=df, date_col='date', base_col='baseline', exp_col='experiment', period='month', path=path)
    get_return_chart_delta_period(df=df, date_col='date', base_col='baseline', exp_col='experiment', period='week', path=path)
    get_return_chart_delta_period(df=df, date_col='date', base_col='baseline', exp_col='experiment', period='year', path=path)
    print('plotting raw chart...')
    plot_chart_from_df(df, 'date', 'baseline', 'experiment', path)



def gen_perf_compare_readable_format(perf_res):
    lines = []
        
    lines.append('===============baseline===============')
    for k,v in perf_res['baseline_perf'].items():
        lines.append(f'{k} {v}')
    lines.append('===============experiment===============')
    for k,v in perf_res['experiment_perf'].items():
        lines.append(f'{k} {v}')
    lines.append('===============Alpha Beta===============')
    for k,v in perf_res['alpha_beta'].items():
        lines.append(f'{k} {v}')

    res = '\n'.join(lines)

    return res


def download_ab_test_asset(baseline_ticket, experiment_ticker, start_date, end_date, path):
    interval = '1d'
    path_baseline = f'{path}{baseline_ticket}.csv'
    path_experiment = f'{path}{experiment_ticker}.csv'
    path_merge = f'{path}merge.csv'
    
    download_format_2csv(baseline_ticket, start_date, end_date, path_baseline, interval)
    download_format_2csv(experiment_ticker, start_date, end_date, path_experiment, interval)
    
    df_base = pd.read_csv(path_baseline)
    df_exp = pd.read_csv(path_experiment)
    
    df_base['date']=df_base.apply(lambda row : unixtime_to_date(row['unixtime']), axis = 1)
    df_exp['date']=df_exp.apply(lambda row : unixtime_to_date(row['unixtime']), axis = 1)
    df_base.rename(columns={'Close':'baseline'}, inplace=True)
    df_exp.rename(columns={'Close':'experiment'}, inplace=True)
    df_base = df_base[['date', 'baseline']]
    df_exp = df_exp[['date', 'experiment']]
    df_merge = pd.merge(df_base, df_exp, on='date')
    df_merge = df_merge.dropna()
    assert not df_merge.isnull().values.any()
    df_merge.to_csv(path_merge, index=False)
    return df_merge



def perf_compare_with_download(baseline_ticket, experiment_ticker, start_date, end_date):
    # create folder
    perf_folder = 'D:/f_data/perf_compare/'
    postfix = gen_random_str()
    root_folder = f'{baseline_ticket}_vs_{experiment_ticker}_{postfix}'
    print(root_folder)
    
    root_path = perf_folder + root_folder
    pic_path = perf_folder + root_folder + '/pic/'
    asset_path = perf_folder + root_folder + '/asset/'
    txt_path = perf_folder + root_folder + '/perf.txt'
    
    os.mkdir(root_path) 
    os.mkdir(pic_path) 
    os.mkdir(asset_path) 
    
    # download stock
    df = download_ab_test_asset(baseline_ticket, experiment_ticker, start_date, end_date, asset_path)
    print(asset_path+'merge.csv')
    
    # compute perf
    print('start compute perf stat')
    r = perf_compare(df, start_date, end_date, txt_path)
    print(r)
    
    # perf chart
    print('start plot chart')
    plot_perf_compare_chart(df, start_date, end_date, pic_path)
    print('done')