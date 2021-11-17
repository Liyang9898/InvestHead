from datetime import date

from operation.lib.ib_parsing_order import ORDER_TYPE_STOP, ORDER_TYPE_LMT
import pandas as pd
from util.util import get_all_csv_file_path_from_folder, sort_dic_by_key, \
    print_sep_line
from version_master.version import op_path_base, op_ib_report_raw, op_record


def get_record_position_quantity():

    df = pd.read_csv(op_record)
    df = df[(df['exit_price'].isnull()) & (df['close date'].isnull())]
    df = df[['ticker', 'quantity', 'enter_price']]
    df.sort_values(by=['ticker'], inplace=True)
    df.reset_index(drop=True, inplace=True)
#     res = df_to_dict_with_key(df, 'ticker', 'quantity')
    res = {}
    for i in range(0,len(df)):
        k = df.loc[i, 'ticker']
        v = {
            'quantity':df.loc[i, 'quantity'], 
            'enter_price':df.loc[i, 'enter_price']
        }
        res[k] = v
    return res


def get_ib_position_quantity():
    record_path = locate_latest_ib_record()
    today = date.today()
    print_sep_line(f"IB position:{record_path} <-----check date (now:{today})")
    record_path_fmt = op_path_base + 'ib_report_fmt/ib_report_fmt.csv'
    file_raw = open(record_path, 'r')
    lines = file_raw.readlines()
    

    lines_position = []
    for line in lines:
        if line.startswith("Open Positions"):
            lines_position.append(line)
            
    file_pos = open(record_path_fmt, 'w')
    file_pos.writelines(lines_position)
    file_pos.close()
    
    df = pd.read_csv(record_path_fmt)
    df = df[df['Account'].notnull()]
    df.to_csv(record_path_fmt, index=False)
    df = df[df['Asset Category']=='Stocks']
    df['quantity'] = df['Quantity'].astype(int)
    df["ticker"] = df["Symbol"].str.lower()
    df = df[['ticker', 'quantity']]
    df.sort_values(by=['ticker'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    res = df_to_dict_with_key(df, 'ticker', 'quantity')
    return res


def df_to_dict_with_key(df, key_col, val_col):

    res = {}
    for i in range(0,len(df)):
        k = df.loc[i, key_col]
        v = df.loc[i, val_col]
        if k not in res.keys():
            res[k] = v
        else:
            res[k] = v + res[k]
    return res


def position_match(ib, record):
    for ticker, ib_quantity in ib.items():
        if ticker not in record.keys():
            print(f"IB: {ticker}:{ib_quantity} not exist in record")
        else:
            if record[ticker]['quantity'] != ib_quantity:
                print(f"IB: {ticker}:{ib_quantity} IB quantity doesn't match record")        

    for ticker, self_ticker_info in record.items():
        self_quantity = self_ticker_info['quantity']
        if ticker not in ib.keys():
            print(f"SELF: {ticker}:{self_quantity} not exist in IB")
        else:
            if ib[ticker] != self_quantity:
                print(f"SELF: {ticker}:{self_quantity} SELF quantity doesn't match IB")      
   
   
def lmt_order_match(manual, ib, take_profit_threshold):
    for ticker, val in manual.items():
        # self list info
        quantity = val['quantity']
        enter_price = val['enter_price']
        lmt_exit_price = enter_price * (1 + take_profit_threshold)
        
        # placed order in IB?
        if ticker not in ib:
            print(f"SELF: {ticker}:{quantity} not exist in IB")
        else:
            if quantity != ib[ticker]['quantity']:
                print(f"SELF: {ticker}: (self){quantity} (ib){ib['ticker']['quantity']} quantity don't match")

            if ib[ticker]['order_type'] == ORDER_TYPE_STOP:
                # price > 1.02
                assert lmt_exit_price >= enter_price * 1.02
            elif ib[ticker]['order_type'] == ORDER_TYPE_LMT:
                # price = 1.04 with +/-0.01 dollar offset
                assert lmt_exit_price - enter_price * 1.04 <= 0.01
                
                
def locate_latest_ib_record():
    files = get_all_csv_file_path_from_folder(op_ib_report_raw)
    dict = {}
    for k,v in files.items():
        k = k[:len(k)-4]
        k = k.split('_')[1]
        dict[k] = v
    
    files_sorted = sort_dic_by_key(dict, descending=True)
    latest_key = list(files_sorted.keys())[0]
    return files_sorted[latest_key]