'''
Created on Jun 9, 2020

@author: leon
'''

# from strategy_lib.strat_ma_trend_20200604 import StrategySimpleMA
import pandas as pd
from indicator_master.constant import trade_summary_interface
from util import util

stock_ticker_with_trade_summary="""D:/f_data/download_yfinance_trades_summary/"""


filepath_list=util.get_all_csv_file_path_from_folder(stock_ticker_with_trade_summary)
print("found "+ str(len(filepath_list))+" ticker with indicator files")

input_file_path="D:/f_data/download_yfinance_trades_summary/"
output_file_path="D:/f_data/download_yfinance_trades_summary_conclusion/trade_summaries.csv"


path_volumn_out = """D:/f_data/volume_all_ticker.csv"""
df_volumn=util.load_df_from_csv(path_volumn_out, ['ticker', 'vol'])

path_company_meta = """D:/f_data/all_ticker/companylist.csv"""
df_company_meta=pd.read_csv(path_company_meta)


map_volumn = {}
for i in range(1, len(df_volumn)):
    map_volumn[df_volumn.loc[i, 'ticker']] = df_volumn.loc[i, 'vol']

map_company_meta = {}
for i in range(1, len(df_company_meta)):
    ticker = df_company_meta.loc[i, 'Symbol']
    cap_str = df_company_meta.loc[i, 'MarketCap']
    company_name = df_company_meta.loc[i, 'Name']
    ipo_year = df_company_meta.loc[i, 'IPOyear']
    sector = df_company_meta.loc[i, 'Sector']
    industry = df_company_meta.loc[i, 'industry']
    map_company_meta[ticker] = {
        'cap': cap_str,
        'company_name': company_name,
        'ipo_year': ipo_year,
        'sector': sector,
        'industry': industry,
    }

 
cnt = 1
dfs = []
for file in filepath_list.keys():
    ticker=util.extract_symbol_name(file)
    print(str(cnt) + " processing: "+ticker+"   "+file)
    cnt = cnt + 1
    df_ts=util.load_df_from_csv(input_file_path+file, trade_summary_interface)
    df_ts['ticker']=ticker
    df_ts['avg_daily_volumn']=0
    #--------------
    df_ts['name']=0
    df_ts['cap']=0
    df_ts['IPOyear']=0
    df_ts['sector']=0
    df_ts['industry']=0
    if ticker in map_volumn.keys():
        df_ts['avg_daily_volumn']=map_volumn[ticker]
 

    if ticker in map_company_meta.keys():
        df_ts['cap']=map_company_meta[ticker]['cap']
        df_ts['sector']=map_company_meta[ticker]['sector']
        df_ts['industry']=map_company_meta[ticker]['industry']
        df_ts['IPOyear']=map_company_meta[ticker]['ipo_year']
        df_ts['name']=map_company_meta[ticker]['company_name']
        
         
    dfs.append(df_ts)
 
result = pd.concat(dfs)
 
print(result)
 
result.to_csv(
    output_file_path,
    columns=['ticker','avg_daily_volumn','name','cap','IPOyear','sector','industry']+trade_summary_interface,
    index=False
)
 
print("to CSV done")
 
print(df_company_meta)
