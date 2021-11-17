'''
Created on Jun 16, 2020

@author: leon
'''
'''
Created on Jun 9, 2020

@author: leon
'''

from indicator_master.indicator_caching_lib import csv2df_indicator


from util import util

from strategy_lib.strat_ma_trend_20200604 import gen_strategy_bundles,StrategySimpleMAFactory
from indicator_master.indicator_compute_lib import tsfilter
from strategy_param_sweep.strategy_param_sweep_lib import strategy_param_sweep

vol_map=util.get_volume_map()
ticker_above_half_million=util.get_ticker_larger_than_vol(500000, vol_map)
print(str(len(ticker_above_half_million))+' ticker above 0.5 M daily avg volume')
stock_ticker_with_indicator_folder="""D:/f_data/download_yfinance_with_indicator/"""


filepath_list=util.get_all_csv_file_path_from_folder(stock_ticker_with_indicator_folder)
print("found "+ str(len(filepath_list))+" ticker with indicator files")

input_file_path="D:/f_data/download_yfinance_with_indicator/"
output_file_path="D:/f_data/download_yfinance_trades_summary_params_sweep/"

start_time="1995-07-26 20:00:00"
end_time="2020-07-26 19:00:00"  

exit_duration_threshiold_set=[3]
exit_profit_threshiold_set=[
    0.005,
    0.01,
    0.015,
    0.02,
    0.025,
    0.03,
    0.035,
    0.04,
    0.05,
    0.06,
    0.08
]

cnt = 0
for file in filepath_list.keys():
    cnt = cnt + 1
    ticker_name=util.extract_symbol_name(file)
    
    # skip all stock which has < 0.1 M volume
    if ticker_name not in ticker_above_half_million:
        print(str(cnt) + ' ' + ticker_name+' <0.5 M avg daily volume, skip')
        continue
    
    newfile = file[:-4] + '_trades_summary_param_sweep.csv'
    print(str(cnt) + " processing: "+file+" -> " + newfile)
    

    # load ticker data with indicator
    df = csv2df_indicator(input_file_path+file)
    #filter time range
    price_with_indicator = tsfilter(df,start_time,end_time)

    # generate strategy_param_bundle_set
    strategy_param_bundle_set = gen_strategy_bundles(exit_duration_threshiold_set, exit_profit_threshiold_set)
    path_out=output_file_path+newfile
    strategy_simple_MA_factory=StrategySimpleMAFactory()
    sweep_result=strategy_param_sweep(
        strategy_simple_MA_factory,
        price_with_indicator,
        strategy_param_bundle_set, 
        path_out
    )
    print(file + '  done')


