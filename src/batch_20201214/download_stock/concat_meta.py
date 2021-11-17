'''
Created on Feb 9, 2020

@author: leon
'''
import pandas as pd
path_swing_result = """D:/f_data/swing_all_stock_20200209.csv"""
def get_all_swing_result():
    path_in = path_swing_result
    path = path_in
    df = pd.read_csv(
        path,
        sep=',',
        header=0,
        names=['ticker','win','lose','total_trades','pnl','win_raw','lose_raw','pnl_raw']
    )
    return df


all_swing_result = get_all_swing_result()
print(all_swing_result)


def get_all_ticker_info():
    path_in = """D:/f_data/all_ticker/companylist.csv"""
    path = path_in
    df = pd.read_csv(
        path,
        sep=',',
        header=0,
        names=['ticker', 'name','last_sale','market_cap','ipo_year','sector','industry','summary_quote','na']
    )
    return df

all_ticker_info = get_all_ticker_info()


def get_all_ticker_vol_info():
    path_in = """D:/f_data/volume_all_ticker.csv"""
    path = path_in
    df = pd.read_csv(
        path,
        sep=',',
        header=0,
        names=['ticker', 'vol']
    )
    return df

all_ticker_vol_info = get_all_ticker_vol_info()
all_ticker_vol_info.dropna(subset=['vol'], inplace=True)

def mark_cap_format(str):
    print(str)
    num_str = str[1:len(str)-1]
    num = float(num_str)
    token = str[len(str)-1:len(str)]
    multiple = 1
    if token == 'M':
        multiple = 1000000
    elif token == 'B':
        multiple = 1000000000
    num = num * multiple 
    return num


def filter(market_cap,vol, pnl, pnl_new, win_raw, win_profit_manager):
    no = None
    if market_cap < 1000000000:
        return no
    if vol < 1000000:
        return no
    if pnl < 0:
        return no
    if pnl_new < 0:
        return no
    if win_raw < 0.5:
        return no
    if win_profit_manager < 0.5:
        return no
    return 'yes'

def format(df):
    df.dropna(subset=['market_cap'], inplace=True)
    df['market_cap']=df.apply(lambda row : mark_cap_format(row['market_cap']), axis = 1)
    df['filter']=df.apply(lambda row : filter(row['market_cap'],row['vol'],row['pnl_raw'],row['pnl'],row['win_raw'],row['win']), axis = 1)
    df.dropna(subset=['filter'], inplace=True)
    
print(all_ticker_info[['ticker', 'name']])


    

#todo
meta_path_out="""D:/f_data/swing_all_stock_20200209_meta.csv"""
swing_result_with_meta = pd.merge(all_swing_result, all_ticker_info,how='inner', on=['ticker'])

swing_result_with_meta_vol = pd.merge(swing_result_with_meta, all_ticker_vol_info, how='inner', on=['ticker'])
format(swing_result_with_meta_vol)

swing_result_with_meta_vol.to_csv(meta_path_out, index=False)
print('done meta')

