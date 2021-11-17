from operation.lib.ib_parsing_order import get_order_dict_from_web_selected_csv
from operation.lib.record_match_lib import get_record_position_quantity, \
    get_ib_position_quantity, position_match, lmt_order_match
from util.util import print_sep_line

# get self record
self_record = get_record_position_quantity()
##################### acquire IB position######################################## 
# step1:account right
# step2:reports->statement->account summary
# step3:select CSV -> download->copy to folder  'D:\f_data\ib_report_raw'
#################################################################################
ib_position_record = get_ib_position_quantity()
##################### acquire IB order######################################## 
# IB: goto: 'orders & trades' -> select right account -> ctrl A 
# -> copy paste in CSV 'D:/f_data/operation/ib_order_raw/'
# name with yyyymmdd.csv using today's date
#################################################################################
ib_order_record = get_order_dict_from_web_selected_csv()
# for x, y in ib_order_record.items():
#     print(x,y)

print_sep_line('Scan Position')
position_match(ib_position_record, self_record)

print_sep_line('Scan Order')
lmt_order_match(manual=self_record, ib=ib_order_record, take_profit_threshold=0.04)

print_sep_line('End')
