import pandas as pd

df_2000 = pd.read_csv('D:/f_data/external_data_source/snapshot_version/russell2000_formatted_yearly.csv')
df_3000 = pd.read_csv('D:/f_data/external_data_source/snapshot_version/russell3000_formatted_yearly.csv')




def find_unmasked_element(all, mask):
    unmasked = []
    for x in all:
        if x not in mask:
            unmasked.append(x)
    return unmasked

def extract_ticker(df, year):
    df2 = df[df['time']==year]
    dic2000=df2.to_dict('records')
    assert len(dic2000) == 1
    ticker2000_str = dic2000[0]['ticker']
    tickers = ticker2000_str.split('|')
    return tickers

def russell_1000(df2000, df3000, year):
    ticker2000=extract_ticker(df2000, year)
    ticker3000=extract_ticker(df3000, year)
    assert len(ticker3000) > len(ticker2000)
    ticker1000=find_unmasked_element(all=ticker3000, mask=ticker2000)
    assert abs(len(ticker1000) - 1000) < 200 # russell element between 800 and 1200
    return ticker1000

rows = []
for y in range(2006,2022):
    tickers = russell_1000(df_2000, df_3000, y)
    ticker_str = '|'.join(tickers)
    row = {'time':y,'cnt':len(tickers),'ticker':ticker_str}
    print(row)
    rows.append(row)

df1000=pd.DataFrame(rows)
df1000.to_csv('D:/f_data/external_data_source/snapshot_version/russell1000_formatted_yearly.csv', index=False)

