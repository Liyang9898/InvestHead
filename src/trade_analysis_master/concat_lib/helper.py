'''
Created on Feb 27, 2021

@author: leon
'''
from batch_20201214.cach_history._multi import idle_position_cash_history
from batch_20201214.reuse_position.reuse_position_lib import reuse_position_cash_history
 
from trade_analysis_master.concat_lib.concat_trades_details import concat_trade_all
 
from trade_analysis_master.concat_lib.summary_process_lib import merge_trade_summaries, conclude_summary
 
 
def all_in_trade_conclude(
    trade_folder, 
    indicator_folder,
    start_time,
    end_time,
    meta
):
      
    # trade detail
    concat_trade_all(trade_folder)
        
    # trade summary
    merge_trade_summaries(trade_folder, meta)
        
    # cash history reuse
    print('===start cash history reuse=====')
    reuse_position_cash_history(
        start_date=start_time.split(' ')[0],
        end_date=end_time.split(' ')[0],
        trade_folder=trade_folder,
        indicator_folder=indicator_folder,
    )
    print('===done cash history reuse=====')
    
    print('===start cash history idle=====')
    idle_position_cash_history(
        start_time,
        end_time,
        trade_folder,
        indicator_folder,
    )
    print('===done cash history idle=====')
      
 
    print('===start gen feature table=====')
#     feature_sub_path = trade_folder + 'feature/'
#     gen_all_sub_feature(indicator_folder, feature_sub_path, trade_folder)
    print('===done gen feature table=====')
     
    #conclude summary
    dic = conclude_summary(trade_folder)
 
    return dic


