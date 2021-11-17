'''
Created on Mar 13, 2021

@author: leon
'''
import os

from batch_20201214.util_for_batch.batch_util import get_all_files
import pandas as pd
from trade_analysis_master.concat_lib.concat_trades_details import join_trades_with_indicator

from version_master.version import indicator_20210301

    
a = get_all_files(indicator_20210301)
print(a)
for x,y in a.items():
    print(x,y)