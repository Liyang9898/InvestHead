from batch_20201214.download_stock.download_stock_lib import download_format_2csv
import pandas as pd
from util.general_ui import plot_lines_from_xy_list
from util.util_pandas import df_normalize
from util.util_portfolio_perf_compare import perf_compare, \
    plot_perf_compare_chart
from util.util_time import unixtime_to_date


start_date = '2010-10-17'
end_date = '2019-10-17'
baseline_ticket = 'spy'
experiment_ticker = 'iwf'

path = 'D:/f_data/hedge/'


def hedge(baseline_ticket, experiment_ticker, start_date, end_date, path):
    # baseline is hedging position, exp is target position
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
    
    df_normalize(df=df_merge, normalize_col='baseline')
    df_normalize(df=df_merge, normalize_col='experiment')
    
    df_merge['hedged'] = (df_merge['experiment'] - df_merge['baseline']) / 2 + 1
    df_merge['experiment'] = df_merge['experiment']
    df_merge['baseline'] = df_merge['baseline']
    
    df_merge.to_csv(path_merge, index=False)
    print(path_merge)
    return df_merge

df_hedged = hedge(baseline_ticket, experiment_ticker, start_date, end_date, path)


df_hedged = pd.read_csv('D:/f_data/hedge/merge.csv')
compared_with_baseline = True

if compared_with_baseline:
    df_hedged.rename(columns={'hedged':'experiment','experiment':'na'}, inplace=True) # vs spy
else:
    df_hedged.rename(columns={'hedged':'experiment','experiment':'baseline'}, inplace=True) # vs iwf

df_hedged = df_hedged[['date','baseline','experiment']].copy()
print(df_hedged)

txt_path = 'D:/f_data/hedge/hedge.txt'

print('start compute perf stat')
r = perf_compare(df_hedged, start_date, end_date, txt_path)
print(r)

# perf chart
pic_path = 'D:/f_data/hedge/pic/'
print('start plot chart')
plot_perf_compare_chart(df_hedged, start_date, end_date, pic_path)
print('done')