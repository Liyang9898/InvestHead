'''
Created on Dec 25, 2020

@author: leon
'''

import os
import pandas as pd 


def merge_trade_summaries(trade_path,meta_path):
    folder_path_trade_results=trade_path + 'summary/'
    trade_summary_bundle_path=trade_path + 'merge/all_trades_summary.csv'

    ticker_meta_with_vol = pd.read_csv(meta_path)
    cnt = 1
    l = []
    for file in os.listdir(folder_path_trade_results):
        if not file.endswith(".csv"):
            continue
          
        # extract ticker
        ticker = file.split('_')[0]
#         print(cnt, ticker)
        # read data
        df = pd.read_csv(folder_path_trade_results+file)
        trade_summary_dic = df.to_dict('records')[0]
        trade_summary_dic['ticker'] = ticker
    #     print(trade_summary_dic)
        l.append(trade_summary_dic)
        cnt=cnt+1    
        
    df_trade_summary_bundle = pd.DataFrame(l)
    if 'Unnamed: 0' in df.columns:
        df_trade_summary_bundle.drop(columns=['Unnamed: 0'], inplace=True)
    
    trade_summary_with_st_info = pd.merge(df_trade_summary_bundle, ticker_meta_with_vol, on='ticker', how='inner')
    
    trade_summary_with_st_info.to_csv(trade_summary_bundle_path, index = False)
    print('written to:', trade_summary_bundle_path)




def conclude_summary(trade_path):
    input_path=trade_path + 'merge/all_trades_summary.csv'
    all_entry_path=trade_path + 'merge/all_trades_all_entry.csv'
    cash_idle_path = trade_path+'merge/cash_history_idle_moving_window.csv'
    cash_alt_path = trade_path+'merge/cash_history_reuse_moving_window.csv'
    
    trading_result = pd.read_csv(input_path)
    df_all_entry = pd.read_csv(all_entry_path)
    cash_idle_res = pd.read_csv(cash_idle_path).to_dict('records')[0]
    cash_alt_res = pd.read_csv(cash_alt_path).to_dict('records')[0]

    enter_opportunity_cnt = len(df_all_entry)
    
    pnl_positive = df_all_entry[df_all_entry['pnl_percent']>0]
    pnl_negative = df_all_entry[df_all_entry['pnl_percent']<0]
    win_opportunity_cnt = len(pnl_positive)
    lose_opportunity_cnt = len(pnl_negative)
    
    win_consecutive = trading_result['win'].sum()
    lose_consecutive = trading_result['lose'].sum()
    total_consecutive = win_consecutive + lose_consecutive
    
    win_pnl_avg_size = pnl_positive['pnl_percent'].mean()
    lose_pnl_avg_size = pnl_negative['pnl_percent'].mean()
    avg_size = df_all_entry['pnl_percent'].mean()
    avg_holding_days = df_all_entry['holding_days'].mean()
    
    
    all_u_avg_win_rate = trading_result['all_universe_win_rate'].mean()
    all_u_avg_lose_rate = trading_result['all_universe_lose_rate'].mean()
    fix = trading_result['total_pnl_fix'].mean()
    roll = trading_result['total_pnl_rollover'].mean()
    win_size = trading_result['average_trade_win_pnl_p'].mean()
    lose_size = trading_result['average_trade_lose_pnl_p'].mean()
    ratio = trading_result['each_trade_win_lose_rate'].mean()
    total_trades = trading_result['total_trades'].mean()

    
    # print(all_u_avg_win_rate,all_u_avg_lose_rate,fix,roll,win_size,lose_size,ratio,total_trades)
    
    
    
    general = {
#         'all_u_avg_win_rate':all_u_avg_win_rate,
#         'all_u_avg_lose_rate':all_u_avg_lose_rate,
        'all_u_win%':win_opportunity_cnt/enter_opportunity_cnt,
        'all_u_lose%':lose_opportunity_cnt/enter_opportunity_cnt,
        'all_u_win_op':win_opportunity_cnt,
        'all_u_lose_op':lose_opportunity_cnt,
        'enter_opportunity_cnt':enter_opportunity_cnt,
        'avg_holding_days':avg_holding_days,
        '|':'|',
        
        'con_win%':win_consecutive/total_consecutive,
        'con_win':win_consecutive,
        'con_lost':lose_consecutive,
        'con_all_cnt':total_consecutive,
        '||':'||',
        
        'avg_single_st_fix':fix+1,
        'avg_single_st_roll':roll,
#         'win_size':win_size,
#         'lose_size':lose_size,
        'win_size':win_pnl_avg_size,
        'lose_size':lose_pnl_avg_size,      
        'avg_size': avg_size,  
        
        'ratio':ratio,
        'total_trades':total_trades,
        '|||':'|||',
    }
    
    all_summary = {}
    
    all_summary.update(general)
    all_summary.update(cash_idle_res)
    all_summary.update(cash_alt_res)
    
    
    df = pd.DataFrame([all_summary])
    df.to_csv(trade_path + 'merge/strat_conclusion.csv', index=False)
    print('written to:', trade_path + 'merge/strat_conclusion.csv')
    
    return all_summary


def conclude_summary2(trade_path):
    input_path=trade_path + 'merge/all_trades_all_entry.csv'
    
    trading_result = pd.read_csv(input_path)
    
    plist = trading_result['pnl_percent'].to_list()
    positive = []
    negative = []
    for p in plist:
        if p > 0:
            positive.append(p) 
        elif p < 0:
            negative.append(p) 
    
    print(len(positive))
    print(len(negative))
    total = len(positive) + len(negative)
    print(len(positive)/total)
#     print(p)
    