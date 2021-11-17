'''
Created on Jul 14, 2020

@author: leon
'''
import pandas as pd
from global_constant.constant import folder_path_trade_ml_sample,trade_feature
from global_constant.constant import folder_path_price_with_indicator,file_type_postfix,folder_path_trade_summary
from indicator_master.constant import trade_summary_interface
from util.util import fist_value_in_dict,percent_str

path_baseline="D:/f_data/trade_summary/BTC_4H_fmt_trade_summary_baseline.csv"
path_cutnarrowstoploss="D:/f_data/trade_summary/BTC_4H_fmt_trade_summary_cutnarrowstoploss.csv"
path_cuttrendend="D:/f_data/trade_summary/BTC_4H_fmt_trade_summary_cuttrendend.csv"
path_cutslowvolicity="D:/f_data/trade_summary/BTC_4H_fmt_trade_summary_cutslowvolicity.csv"
path_cuttrendend_narrowstoploss="D:/f_data/trade_summary/BTC_4H_fmt_trade_summary_cuttrendend_narrowstoploss.csv"
path_cuttrendend_narrowstoploss_lowv="D:/f_data/trade_summary/BTC_4H_fmt_trade_summary_cuttrendend_narrowstoploss_lowv.csv"
path_cuttrendend_slowv="D:/f_data/trade_summary/BTC_4H_fmt_trade_summary_cuttrendend_slowvolicity.csv"

path_05="D:/f_data/trade_summary/BTC_4H_fmt_trade_summary_05.csv"
path_04="D:/f_data/trade_summary/BTC_4H_fmt_trade_summary_04.csv"


def read_trade_summary(path):
    df = pd.read_csv(
        path,
        sep=',',
        header=0,
        names=trade_summary_interface
    )
    dic=df.to_dict()
    fist_value_in_dict(dic)
    return dic

trade_baseline = read_trade_summary(path_baseline)
trade_cutnarrowstoploss = read_trade_summary(path_cutnarrowstoploss)
trade_cuttrendend = read_trade_summary(path_cuttrendend)
trade_cutslowvolicity = read_trade_summary(path_cutslowvolicity)
trade_cuttrendend_narrowstoploss = read_trade_summary(path_cuttrendend_narrowstoploss)
trade_cuttrendend_narrowstoploss_lowv = read_trade_summary(path_cuttrendend_narrowstoploss_lowv)
trade_cuttrendend_slowv = read_trade_summary(path_cuttrendend_slowv)
trade_05 = read_trade_summary(path_05)
trade_04 = read_trade_summary(path_04)

def compare(base, exp):
    win_count_delta = (exp['win'] - base['win'])/base['win']
    lose_count_delta = (exp['lose'] - base['lose'])/base['lose']
    print('win_cnt:',base['win'],'  lose_cnt:', base['lose'])
    print('win_cnt_change:',exp['win'] - base['win'], '  lose_cnt_change:',exp['lose'] - base['lose'])
    print('win_cnt_change:',percent_str(win_count_delta), '  lose_cnt_change:',percent_str(lose_count_delta), 'effective_ratio:',lose_count_delta/win_count_delta)
    print('trade cut:', percent_str((exp['total_trades']-base['total_trades'])/base['total_trades']))
    print()
    win_rate_delta = exp['win_rate'] - base['win_rate']
    lose_rate_delta = exp['lose_rate'] - base['lose_rate']
    
    print('win_rate:', percent_str(base['win_rate']),'lose_rate:', percent_str(base['lose_rate']))
    print('win_rate_change:', percent_str(win_rate_delta),'lose_rate_change:', percent_str(lose_rate_delta))
    print()
    pnl_p_delta = (exp['win_pnl_p']+exp['lose_pnl_p'])-(base['win_pnl_p']+base['lose_pnl_p'])
    print('pnl:',percent_str(base['win_pnl_p']+base['lose_pnl_p']))
    print('pnl_change:',percent_str(pnl_p_delta))
    print("=======================================================================================================")

print("cuttrendend")
compare(trade_baseline, trade_cuttrendend)    
print("cutnarrowstoploss")
compare(trade_baseline, trade_cutnarrowstoploss)
print("cutslowvolicity")
compare(trade_baseline, trade_cutslowvolicity)
print("cuttrendend_narrowstoploss")
compare(trade_baseline, trade_cuttrendend_narrowstoploss)
print("cuttrendend_narrowstoploss_lowv")
compare(trade_baseline, trade_cuttrendend_narrowstoploss_lowv)
print("trade_cuttrendend_slowv")
compare(trade_baseline, trade_cuttrendend_slowv)

print("05 vs 04")
compare(trade_05, trade_04)


