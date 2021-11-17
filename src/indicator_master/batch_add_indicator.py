from indicator_master.lib.batch_gen_indicator import batch_gen_indicator
from version_master.version import (
    price_asset_path_base,
)


price_file_path = price_asset_path_base + '2021-07-03/format/'
print(price_file_path)
indicator_folder_name = '20210704_swing_only'

start_time='2020-01-01'
end_time='2021-07-03'
    
# it will delete and create a new indicator_folder_name
batch_gen_indicator(price_file_path, indicator_folder_name, start_time, end_time)   