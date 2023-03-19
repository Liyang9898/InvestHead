'''
Created on Feb 26, 2023

@author: spark
'''
from functools import reduce
import plotly.express as px

import pandas as pd
from random_research.try_20230224.perf_lib import plot
from util.general_ui import plot_bar_set_from_xy_list
from util.general_ui import plot_lines_from_xy_list
from util.util_finance import get_alpha_beta_from_list
from util.util_pandas import df_general_time_filter, df_normalize
from util.util_pandas import get_year_begin_rows, get_pnl_between_rows, get_month_begin_rows


# spy benchmark
spy_path = "C:/f_data/price_with_indicator/SPY_1D_fmt_idc.csv"
df_spy_base = pd.read_csv(spy_path)

for year in range(2006,2023):
    df_spy = df_spy_base.copy()
    end_year = year+1
    
    start_date = '{s}-01-01'.format(s=year)
    end_date = '{e}-01-01'.format(e=end_year)
    
    title = start_date + ' to ' + end_date
    print(title)
    
    df_spy = df_general_time_filter(df_spy, 'date', start_date, end_date)
    
    df_spy_normalize = df_normalize(df_spy, 'close', initial_val=1)
    df_spy_normalize['spy'] = df_spy_normalize['close']
    df_spy_normalize = df_spy_normalize[['date', 'spy']]
    df_spy_normalize = df_spy_normalize.copy()
    
    # test set
    # test_path = 'C:/f_data/sector/result/spy_rebuild.csv'
    
    
    # experiment_name
    # experiment_name = "allocation_ema21_below_ma50"
    # experiment_name = "allocation_ema21_below_ma50_alpha_ranked"
    # experiment_name = "allocation_ema21_below_ma50_alpha_calibrated_ranked"
    # experiment_name = "allocation_ema21_below_ma50_alpha_calibrated_ranked_delete_neg"
    # experiment_name = "allocation/allocation_ema21_below_ma50_recent_pnl_ranked"
    # experiment_name = "allocation_ema21_below_ma50_recent_pnl_ranked_top3"
    # experiment_name = "allocation_ema21_below_ma50_recent_pnl_past_1_month_ranked_top3"
    # experiment_name = "allocation_ema21_below_ma50_recent_pnl_past_1_month_ranked_top3_precompute"
    # experiment_name = "weekly_allocation_ema21_below_ma50_recent_pnl_past_1_month_ranked_top3_precompute"
    experiment_name = "allocation_ema21_below_ma50_recent_pnl_past_1_month_ranked_top3_increase_only"

    test_path = "C:/f_data/sector/result/{experiment_name}.csv".format(experiment_name=experiment_name)
    test_path_sector = "C:/f_data/sector/result_sector/{experiment_name}.csv".format(experiment_name=experiment_name)

    
    
    df_test = pd.read_csv(test_path)
    df_test = df_general_time_filter(df_test, 'date', start_date, end_date)
    df_test = df_normalize(df_test, 'ts', initial_val=1)
    
    # plot
    df_merge = reduce(lambda df1,df2: pd.merge(df1,df2,on='date'), [df_spy_normalize, df_test])
    x_list = df_merge['date'].to_list()
    y_list_map = {'test': df_merge['ts'].to_list(), 'spy': df_merge['spy'].to_list()}
    
    plot_lines_from_xy_list(x_list=x_list, y_list_map=y_list_map, title=title, path=None)
    
    ppp = 'C:/f_data/sector/result/merge.csv'
    df_merge.to_csv(ppp, index=False)


    ### sector
    df_test2 = pd.read_csv(test_path)
    df_test2 = df_general_time_filter(df_test2, 'date', start_date, end_date)
    
    # sector_aum_path = 'C:/f_data/sector/debug/sector_line.csv'
    df_sector_aum = pd.read_csv(test_path_sector)
    df_sector_aum = df_general_time_filter(df_sector_aum, 'date', start_date, end_date)
    
    # join df_test2 & df_sector_aum
    df_test2['ticker'] = 'AUM total'
    print(df_test2.columns)
    print(df_sector_aum.columns)
    
    df_pic = pd.concat([df_test2, df_sector_aum], axis=0, ignore_index=True)
    
    # df_test = df_normalize(df_test, 'ts', initial_val=1)
    fig_sector = px.scatter(df_pic, x="date", y="ts", color='ticker', title='sector_remix')
    fig_sector.show()      
