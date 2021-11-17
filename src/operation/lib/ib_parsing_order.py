from datetime import date

import pandas as pd
from util.util import get_all_csv_file_path_from_folder, sort_dic_by_key, \
    print_sep_line
from version_master.version import (
    op_ib_order_raw,
)

ORDER_TYPE_STOP = 'Stop'
ORDER_TYPE_LMT = 'Limit'


def latest_file():
    files = get_all_csv_file_path_from_folder(op_ib_order_raw)
    files_sorted = sort_dic_by_key(files, descending=True)
    latest_key = list(files_sorted.keys())[0]
    return files_sorted[latest_key]


def line_validator(line):   
    if line.find("Sell") >= 0 and (line.find(ORDER_TYPE_LMT) >= 0 or line.find(ORDER_TYPE_STOP) >= 0):
        return True
    else:
        return False


def line_processor(line):
    # high level process
    tokens = line.split(',')
    ticker = tokens[0].lower()
    order_detail_token = tokens[1].split(' ')
    
    assert order_detail_token[0] == 'Sell'
    order_fill = tokens[2]
    
    # GTC validation
    assert order_detail_token[len(order_detail_token)-1] == 'GTC'
    
    # quantity process
    quantity = int(order_fill.split('/')[1])
    assert quantity == int(order_detail_token[1])
    
    
    # order type
    order_type = order_detail_token[2] # we only place limit and stop limit order
    
    # process and validate limit order
    
    if order_type == ORDER_TYPE_LMT:
        assert len(order_detail_token) == 5
        price = float(order_detail_token[3])
    elif order_type == ORDER_TYPE_STOP:
        assert len(order_detail_token) == 7
        assert order_detail_token[4] == 'LMT' 
        assert order_detail_token[3] == order_detail_token[5]
        price = float(order_detail_token[3])
    else:
        raise ValueError(f'Unknown order type{tokens[1]}')
    
    row = {
        'ticker':ticker,
        'quantity':quantity,
        'price':price,
        'order_type':order_type,
    }
    
    return row


def filter_line(file_raw):
    file_raw = open(file_raw, encoding="utf8")
    lines = file_raw.readlines()

    rows = []
    for line in lines:
        if line_validator(line):
            order_detail = line_processor(line)
            rows.append(order_detail)
    df = pd.DataFrame(rows)
    return df


def order_df_to_fict(df):
    res = {}
    for idx in range(0,len(df)):
        ticker = df.loc[idx, 'ticker']
        if ticker in res.keys():
            raise Exception('Duplicate ticker in order: ' + ticker) 
        res[ticker] = {
            'quantity': df.loc[idx, 'quantity'],
            'price': df.loc[idx, 'price'],
            'order_type': df.loc[idx, 'order_type']      
        }

    return res

def get_order_dict_from_web_selected_csv():
    # IB: goto: 'orders & trades' -> select right account -> ctrl A 
    # -> copy paste in csv 'D:/f_data/operation/ib_order_raw/'
    # name with yyyymmdd.csv using today's date
    file_raw = latest_file()
    today = date.today()
    print_sep_line(f"IB order:{file_raw} <-----check date (now:{today})")
    order_df = filter_line(file_raw)
    order_dic = order_df_to_fict(order_df)
    return order_dic
