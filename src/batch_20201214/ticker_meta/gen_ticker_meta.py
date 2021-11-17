import pandas as pd 
from _ast import And

def mark_cap_format(input):
    str2 = str(input)
    
    # less than 1 M
    last_char = str2[len(str2)-1]
    if last_char != 'M' and last_char != 'B':
        return

    if len(str2)<=0 or str2 == 'nan':
        return
    
    
    num_str = str2[1:len(str2)-1]
    num = float(num_str)
    token = str2[len(str2)-1:len(str2)]
    multiple = 1
    if token == 'M':
        multiple = 1000000
    elif token == 'B':
        multiple = 1000000000
    num = num * multiple 
    return num

# daily stock vol
ticker_vol = pd.read_csv("""D:/f_data/sweep_20201214/all_ticker_meta/volume_all_ticker_20210108.csv""")
print(ticker_vol)

# MA50_ uprate
path_ma50_up_rate = "D:/f_data/sweep_20201214/all_ticker_meta/ma50_up_rate_20210117.csv"
ma50_uprate_df = pd.read_csv(path_ma50_up_rate)

#stock meta
#where you download stock
#https://stackoverflow.com/questions/25338608/download-all-stock-symbol-list-of-a-market
ticker_meta = pd.read_csv("D:/f_data/sweep_20201214/all_ticker_meta/ticker_raw/ticker_all_20210106.csv")
print(ticker_meta)
ticker_meta['ticker']=ticker_meta['Symbol']


ticker_meta_with_vol = pd.merge(ticker_meta, ticker_vol, on='ticker', how='inner')
ticker_meta_with_vol_ma_50_up = pd.merge(ticker_meta_with_vol, ma50_uprate_df, on='ticker', how='inner')
ticker_meta_with_vol_ma_50_up.drop(columns=['Symbol'], inplace=True)
ticker_meta_with_vol_ma_50_up['MarketCapNum']=ticker_meta_with_vol_ma_50_up.apply(lambda row : mark_cap_format(row['MarketCap']), axis = 1)
print(ticker_meta_with_vol_ma_50_up)

ticker_meta_with_vol_ma_50_up.to_csv('D:/f_data/sweep_20201214/all_ticker_meta/20210117_ticker_meta_with_vol.csv',index = False)