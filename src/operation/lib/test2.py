from datetime import datetime
from datetime import datetime

from batch_20201214.util_for_batch.batch_util import get_all_files
from indicator_master.plot_indicator_lib import plot_indicator
import pandas as pd
from strategy_lib.strat_ma_swing import StrategySimpleMA
from trading_floor.EntryPointGenerator import gen_entry
from version_master.version import op_path_base
from version_master.version import op_path_base, op_record


# from version_master.version import op_path_indicator
path = 'D:/f_data/operation/2021-03-25/indicator/MORN_downloaded_raw.csv'
df_range = pd.read_csv(path)

plot_indicator(df_range, 'sequence_8_21_50')