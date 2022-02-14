import norgatedata
import pandas as pd


def extract_year(d):
    d = str(d)
    year=d.split('-')[0]
    return year
    

def extract_index_present_year_from_df(df):
    df = df[df['Index Constituent'] == 1].copy()
    df.reset_index(inplace=True)
    if len(df) == 0:
        return []
    df['year']=df.apply(lambda row : extract_year(row['Date']), axis = 1)
    df = df.sort_values(by='year', ascending=True)
    year_all = df['year'].unique()
    return year_all


def get_ticker_present_year_in_index(ticker, index_name):
    timeseriesformat = 'pandas-dataframe'
    priceadjust = norgatedata.StockPriceAdjustmentType.TOTALRETURN
    padding_setting = norgatedata.PaddingType.NONE

    pricedata_df = norgatedata.price_timeseries(
        ticker,
        stock_price_adjustment_setting = priceadjust,
        padding_setting = padding_setting,
        timeseriesformat = timeseriesformat,
    )
     
    # and now make the call to index_constituent_timeseries
    pricedata_df_index_mark = norgatedata.index_constituent_timeseries(
        ticker,
        index_name,
        padding_setting = padding_setting,
        limit = -1,
        pandas_dataframe = pricedata_df,
        timeseriesformat = timeseriesformat,
    )
    
    # extract year
    all_year = extract_index_present_year_from_df(pricedata_df_index_mark)
    return all_year


def get_ticker_present_index_year(watchlistname):
    """
    input: index and its attribute, ex:'S&P 500 Current & Past'
    output: input: dataframe cols = ticker, year_cnt, years
    """
    tickers = norgatedata.watchlist_symbols(watchlistname)
    print(len(tickers), 'ticker_cnt')
    cnt = 1
#     yearly_index = {} # dict<year, list<ticker>>
    rows = []
    for ticker in tickers:
#         if cnt < 1595:
#             print(cnt)
#             cnt += 1
#             continue

        index_name = 'S&P 500' 
        all_year = get_ticker_present_year_in_index(ticker, index_name)
        all_year_str = '|'.join(all_year)
        row = {'ticker':ticker, 'year_cnt':len(all_year), 'all_year':all_year_str}
        print(cnt, row)
        rows.append(row)
        cnt = cnt + 1

    df = pd.DataFrame(rows)
    return df


def format_yearly_index(df):
    """
    input: dataframe cols = ticker, year_cnt, years
    output: dataframe of yearly index, cols = [time, cnt, ticker]
    """
    yearly_index = {}
    for i in range(0, len(df)):
        ticker = df.loc[i, 'ticker']
        years = df.loc[i, 'all_year']
        cnt = df.loc[i, 'year_cnt']
        
        years_list = []
        if cnt >=2:
            years_list = years.split('|')
        elif cnt == 1:
            years_list = [years]
        
        
        for year in years_list:
            if year not in yearly_index.keys():
                yearly_index[year] = []
            yearly_index[year].append(ticker)
    
    rows = []
    for year, tickers in yearly_index.items():
        tickers_str = '|'.join(tickers)
        cnt = len(tickers)
        row = {'time':year, 'cnt':cnt, 'ticker':tickers_str}
        print(cnt, row)
        rows.append(row)
    df = pd.DataFrame(rows)   
    df = df.sort_values(by='time', ascending=True)
    return df 


# get all past and current ticker in index
watchlistname = 'S&P 500 Current & Past'

path_ticker_year = 'D:/f_data/external_data_source/snapshot_version/sp500_ticker_year.csv'
ticker_present_year_df = get_ticker_present_index_year(watchlistname)
ticker_present_year_df.to_csv(path_ticker_year, index=False)

path_yearly_index_spy = 'D:/f_data/external_data_source/snapshot_version/sp500_formatted_yearly.csv'
df_ticker_year = pd.read_csv(path_ticker_year)
df_yearly_index = format_yearly_index(df_ticker_year)
df_yearly_index.to_csv(path_yearly_index_spy, index=False)

