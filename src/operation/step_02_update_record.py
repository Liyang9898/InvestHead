from operation.lib.migrate_close import move_closed_positions, back_up_record, \
    file_closed_check
from operation.lib.summary import get_portafolio_summary
from operation.lib.trade_lib import update_record_current_price
from version_master.version import op_path_base
from datetime import datetime


now = datetime.today()
now_str = now.strftime('%Y-%m-%d')
path_base = op_path_base + now_str
op_path_indicator = path_base + '/indicator/'

# make sure all files (record.csv, closed csv) are closed
file_closed_check()

# back up record before move close and updated
back_up_record()

# move closed position over
move_closed_positions()

# update stock price in current record.csv
update_record_current_price(op_path_indicator)

# print summary
print(get_portafolio_summary())