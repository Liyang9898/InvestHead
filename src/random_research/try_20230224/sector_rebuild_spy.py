'''
Created on Feb 24, 2023

@author: spark
'''
import pandas as pd
import plotly.express as px

def get_year(date):
    date_str = str(date)
    year = int(date_str.split('-')[0])
    return year


def get_one_sector_ts_scaled(df_sector, year, initial_aum):
    '''
    Step 1: get ts from sector
    Step 2: trim to year
    Step 3: reweight to match initial aum
    '''
    
    df_sector = df_sector[df_sector['year']==year]
    df_sector = df_sector.copy()
    
    df_sector.reset_index(inplace=True, drop=True)
    factor = initial_aum / df_sector.iloc[0]['close']
    df_sector['ts'] = df_sector['close'] * factor
    
    return df_sector



ticker = 'XLK'
sector_idc_path = "C:/f_data/sector/indicator/{ticker}_1W_fmt_idc.csv".format(ticker=ticker)  

df = pd.read_csv(sector_idc_path)
df['year']=df.apply(lambda row : get_year(row['date']), axis = 1)
print(df['year'])
year = 2020
initial_aum = 0.13

df = get_one_sector_ts_scaled(df, year, initial_aum)
print(df[['date','ts']])

# fig = px.line(df, x="date", y="ts", title='mudong op timeseries')
# fig.show()


tickers = []

path = 'C:/f_data/sector/spy_sector_history.csv'
df = pd.read_csv(path)
print(df)

years = [2019,2020,2021]
record = df.to_dict('records')
allocation = {}
for r in record:
    print(r)
    ticker = r['ticker']
    allocation[ticker] = {}
    tickers.append(ticker)
    for year in years:
        aum_str = r[str(year)]
        aum_str = aum_str.replace("%", "")
        aum = float(aum_str) * 0.01
        allocation[ticker][year] = aum

        
    
print(allocation)




