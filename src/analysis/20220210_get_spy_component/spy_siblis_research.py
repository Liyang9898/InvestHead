import pandas as pd
import re


def date_year_fixer(d):
    tokens = d.split('-')
    d = tokens[0]

    d = int(d)
    if d > 2023:
        d = d - 100
    return str(d)


def ticker_formatter(ticker_str):
    """
    if input is Empty, return None
    if input is -, return None
    if () is included, remove the content within it
    """

    if len(ticker_str) == 0 or ticker_str == '-':
        return None
    
    
    ticker_str_no_space = ticker_str.replace(" ", "")
    l = ticker_str_no_space.find('(')
    if l!=-1:
        ticker_str_no_space = ticker_str_no_space[:l]
    
    return ticker_str_no_space
#     pattern = re.compile("[A-Za-z]+")
#     if not pattern.fullmatch(ticker_str_no_space):
#         print(ticker_str_no_space)


path = 'D:/f_data/external_data_source/spy_components/sp500_clean_csv.csv'
path_dt_format = 'D:/f_data/external_data_source/spy_components/sp500_clean_dt_format_csv.csv'
df = pd.read_csv(path)
df['date_fmt'] = df['date'].astype('datetime64[ns]')
df['date_fmt'] = df['date_fmt'].astype('str')
df['date_fmt']=df.apply(lambda row : date_year_fixer(row['date_fmt']), axis = 1)
df = df.sort_values(by='date_fmt', ascending=True)
df.reset_index(inplace=True, drop=True)
df.to_csv(path_dt_format, index=False)

spy_snapshot = {}
cur_spy = []
pre_date = '-1'
for i in range (0, len(df)):
    ticker_add = df.loc[i, 'ticker_add']
    ticker_remove = df.loc[i, 'ticker_remove']
    date = df.loc[i, 'date_fmt']
    ticker_add = ticker_formatter(ticker_add)
    ticker_remove = ticker_formatter(ticker_remove)
    
#     print(ticker_add, ticker_remove, date)
    

    # take action
    if ticker_add != None:
        cur_spy.append(ticker_add)
    if ticker_remove != None: 
        if ticker_remove in cur_spy:
            cur_spy.remove(ticker_remove)
        else:
            print('cant remove', date, ticker_remove, df.loc[i, 'date'], len(cur_spy))

    
    
