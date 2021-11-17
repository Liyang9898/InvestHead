
from external_data.index_constituents.change_set_to_time_snapshot import constituents_change_to_time_snapshot
from external_data.index_constituents.index_constituents_lib import  date_format_convert_russell2000, date_format_convert_russell3000, ticket_format
import pandas as pd


# load data 2000
path_2000 = 'D:/f_data/external_data_source/snapshot_version/russell2000.csv'
df_2000 = pd.read_csv(path_2000)

# load data 3000
path_3000 = 'D:/f_data/external_data_source/snapshot_version/russell3000.csv'
df_3000 = pd.read_csv(path_3000)


def extract_tickers_given_time(df, t_col):
    df=df[['ticker', t_col]]
    df = df.copy()
    df = df.dropna()
    tickers = df['ticker'].to_list()
    return tickers


def gen_snapshot_timeseries(df):
    rows = []
    non_time_cols = [
        'ticker',
        'company_name',
        'ISIN Code',
        'Sector'
    ]
    
    time_cols = []
    for x in df.columns:
        if x not in non_time_cols:
            time_cols.append(x)
    
    for time in time_cols:
        tickers_raw = extract_tickers_given_time(df, time)
        # format ticker
        tickers=[]
        for t in tickers_raw:
            t_fmt = ticket_format(t)
            tickers.append(t_fmt)
        tickers_str = '|'.join(tickers)
        row = {'time':time,'cnt':len(tickers),'ticker':tickers_str}
        rows.append(row)
    df = pd.DataFrame(rows)
    print(df)
    return df
        
df_2000_td = gen_snapshot_timeseries(df=df_2000)
df_2000_td.to_csv('D:/f_data/external_data_source/snapshot_version/russell2000_formatted.csv', index = False)
df_3000_td = gen_snapshot_timeseries(df=df_3000)
df_3000_td.to_csv('D:/f_data/external_data_source/snapshot_version/russell3000_formatted.csv', index = False)