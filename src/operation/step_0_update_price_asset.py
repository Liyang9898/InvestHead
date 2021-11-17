from operation.lib.migrate_close import move_closed_positions, back_up_record, \
    file_closed_check
from operation.lib.price_asset_lib import refresh_price_asset
from operation.lib.summary import get_portafolio_summary
from version_master.version import swing_set1



file_closed_check()
 
back_up_record()
move_closed_positions()
refresh_price_asset(time_window=100, set_list=swing_set1)

print(get_portafolio_summary())