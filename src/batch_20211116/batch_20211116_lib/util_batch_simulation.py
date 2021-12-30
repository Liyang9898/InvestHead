from dataclasses import replace
from datetime import datetime

from api.api import api_download_ticker
import pandas as pd
from util.general_ui import plot_points_from_xy_list
from util.util_time import df_filter_dy_date


def get_benchmark(ticker, start_date, end_date):
    start = start_date
    end = end_date
    interval = '1d'

    path = 'D:/f_data/temp/spy20211207.csv'
    api_download_ticker(ticker, start, end, path, interval)
    df = pd.read_csv(path)
    
    df['date']=df.apply(lambda row : str(datetime.fromtimestamp(int(row['unixtime'])).strftime('%Y-%m-%d')), axis = 1)
    df[ticker] = df['Close']
    base = df.loc[0,ticker]
    df[ticker] = df[ticker] / base
    df=df[['date',ticker]]
    df=df.copy()
    return df


def normalized_position(df, time_col, value_col):
    """
    This function will make the begining of the time series = 1
    """
    assert pd.Index(df[time_col]).is_monotonic == True
    factor = df.loc[0, value_col]
    df[value_col] = df[value_col] / factor


def position_time_series_append_benchmark_to_csv_png(
    position_time_series_csv,
    input_time_col,
    input_position_col,
    start_date,
    end_date,
    benchmark_ticker,
    output_time_series_csv,
    output_time_series_png
):
    """
    this function download a benchmark ticker, pair with your position time series
    do normalization on start = 1, and output
    input: position_time_series
    output: position_time_series + benchmark csv and png
    """
    # get benchmark time series
    portfolio_df = pd.read_csv(position_time_series_csv)
    portfolio_df = df_filter_dy_date(portfolio_df,'date',start_date,end_date)
    
#     end_date = portfolio_df[input_time_col].max()
#     start_date = portfolio_df[input_time_col].min()
    benchmark_df = get_benchmark(benchmark_ticker, start_date, end_date)
    
    # merge
    m_result = pd.merge(portfolio_df, benchmark_df, how="inner", on="date")
    
    # clean
    m_result['portfolio'] = m_result[input_position_col]
    m_result = m_result[['date', 'portfolio', benchmark_ticker]].copy()
    m_result.sort_values(by=input_time_col, ascending=True, inplace=True)
    normalized_position(m_result, input_time_col, 'portfolio')
    normalized_position(m_result, input_time_col, benchmark_ticker)

    # output csv
    m_result.to_csv(output_time_series_csv, index=False)
    
    # output png
    x_list = m_result[input_time_col].to_list()
    y_list = {
        'portfolio':m_result['portfolio'].to_list(),
        benchmark_ticker:m_result[benchmark_ticker].to_list()
    }
    title = 'Position Time Series'
    plot_points_from_xy_list(x_list, y_list,title,output_time_series_png)
    

def merge_dic(list_of_dict):
    res = {}
    for d in list_of_dict:
        for k,v in d.items():
            if k in res:
                raise Exception(f'{k}:key already exist')
            res[k] = v
    return res


def major_filter(dic):
    res = {}
    for k in dic.keys():
        if 'major' in k or 'ticker' in k:
            res[k] = dic[k]
    return res
    
def two_dict_merge_value_to_list(dict1, dict2):
    """
    merge 2 dict into one, their value under the same key will be stored in a list
    """
    res = {}
    for k, v in dict1.items():
        if k not in res.keys():
            res[k] = []
        res[k].append(v)
    for k, v in dict2.items():
        if k not in res.keys():
            res[k] = []
        res[k].append(v)
    return res
    
    
def strategy_baseball_card(
    position_perf_csv,
    trade_perf_csv,
    year_alpha_beta_csv,
    month_alpha_beta_csv,
    baseball_card_csv,
):
    """
    this is a csv formatter
    """
    position_perf_df = pd.read_csv(position_perf_csv)
    trade_perf_df = pd.read_csv(trade_perf_csv)
    year_alpha_beta_df = pd.read_csv(year_alpha_beta_csv)
    month_alpha_beta_df = pd.read_csv(month_alpha_beta_csv)
    
    position_perf_dic = position_perf_df.to_dict('records')
    trade_perf_dic = trade_perf_df.to_dict('records')[0]
    year_alpha_beta_dic = year_alpha_beta_df.to_dict('records')[0]
    month_alpha_beta_dic = month_alpha_beta_df.to_dict('records')[0]
    
    
    # reformat data
    port_position_perf = position_perf_dic[0]
    bench_position_perf = position_perf_dic[1]
    if position_perf_dic[1]['ticker'] == 'portfolio':
        port_position_perf = position_perf_dic[1]
        bench_position_perf = position_perf_dic[0]
        
    year_alpha_beta_dic = {'year_'+ k :v for k,v in year_alpha_beta_dic.items()}
    month_alpha_beta_dic = {'month_'+ k :v for k,v in month_alpha_beta_dic.items()}
    del trade_perf_dic['ticker']
    port_position_perf = major_filter(port_position_perf)
    bench_position_perf = major_filter(bench_position_perf)
            
    
#     print(port_position_perf)
#     print(bench_position_perf)
#     print(trade_perf_dic)
#     print(year_alpha_beta_dic)
#     print(month_alpha_beta_dic)
    
    # merge
    list_of_dict = [
        port_position_perf,
        trade_perf_dic,
        year_alpha_beta_dic,
        month_alpha_beta_dic
    ]
    port_baseball_dic = merge_dic(list_of_dict)
    baseball_dic = two_dict_merge_value_to_list(port_baseball_dic, bench_position_perf)
    
    # save to csv output
    res_df = pd.DataFrame.from_dict(data=baseball_dic, orient='index')
    res_df.reset_index(inplace=True)
    res_df.to_csv(baseball_card_csv, index=False, header=None)
