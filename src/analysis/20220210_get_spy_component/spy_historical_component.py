import pandas as pd

# clean the historical spy component csv
path = 'D:/f_data/external_data_source/spy_components/sp500_history.txt'
path_clean = 'D:/f_data/external_data_source/spy_components/sp500_history_clean.csv'
df = pd.read_csv(path)
df = df[['date', 'ticker', 'name', 'action', 'cik']]
df['date_fmt'] = df['date'].astype('datetime64[ns]')
df['date_fmt'] = df['date_fmt'].astype('str')
df = df.sort_values(by='date_fmt', ascending=True)
df.reset_index(inplace=True, drop=True)
df.to_csv(path_clean, index=False)
# print(df)

spy_snapshot = {}
cur_spy = []
pre_date = '-1'
for i in range(0, len(df)):
    date = df.loc[i, 'date_fmt']
    ticker = df.loc[i, 'ticker']
    action = df.loc[i, 'action']
    print(date, ticker, action)
    
    # new date showed up wrap up previous date
    if date != pre_date:
        snapshot = cur_spy.copy()
        spy_snapshot[pre_date] = snapshot
        pre_date = date
        
    # take action
    if action == 'added':
        cur_spy.append(ticker)
    elif action == 'removed':
        if ticker in cur_spy:
            cur_spy.remove(ticker)

snapshot = cur_spy.copy()
spy_snapshot[pre_date] = snapshot
pre_date = date

for d, spy in spy_snapshot.items():
    print(d, len(spy))