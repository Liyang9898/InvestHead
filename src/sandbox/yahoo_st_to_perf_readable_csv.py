import pandas as pd
from util.util_time import unixtime_to_date

root_path = 'D:/f_data/price_asset/2021-10-06/format/'
root_path_out = 'D:/f_data/temp/jp_portfolio/'

ticker_list = [
    'iwf', 
    'JLGMX',
    'JMGMX',
    'JGSMX',
    'JSDRX'
]

strategy_name='strat_param_20211006_ma_max_drawdown_cut'
path_position_record = f'D:/f_data/temp/position_list_{strategy_name}.csv'
df_base_raw = pd.read_csv(path_position_record)
df_base = df_base_raw[['date', 'experiment']].copy()
df_base.rename(columns={'experiment':'baseline'}, inplace=True)
# print(df_base)

for ticker in ticker_list:
    path_in = root_path+ticker+'_downloaded_raw.csv'
    path_out = root_path_out+ticker+'_downloaded_raw.csv'
    df = pd.read_csv(path_in)
    df['date']=df.apply(lambda row : unixtime_to_date(row['time']), axis = 1)
    df=df[['date','close']].copy()
    df.rename(columns={'close':'experiment'}, inplace=True)
    print(df)
    df_merge = pd.merge(df_base, df, how="inner",on='date')
    assert len(df_merge)<=len(df_base)
    
    df_merge.to_csv(path_out, index=False)
