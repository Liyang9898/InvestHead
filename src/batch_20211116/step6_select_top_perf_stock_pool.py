from batch_20211116.batch_20211116_lib.constant import TRADE_SUMMARY_ALL_TICKER, ranked_ticker_path
import pandas as pd
from util.util_file import get_all_csv_file_in_folder
from util.util_math import intersection_of_k_list

PERF_COLS = ['ma50_up_rate', 'win_rate', 'annual_avg_return', 'win_lose_pnl_ratio', 'total_trades_all_entry']


       
def basic_filter(df):
    df = df[
        (df['ma50_up_rate'] > 0.5) & 
        (df['win_rate'] > 0.5) & 
        (df['annual_avg_return'] > 0.03) & 
        (df['win_lose_pnl_ratio'] > 1.1) & 
        (df['total_trades_all_entry'] > 10)
    ]

    df = df.copy()
    df.reset_index(inplace=True, drop=True)
    return df


def rank_ticker_by_col(df, col):
    rank = {}
    df = df[['ticker', col]]
    df_sort = df.copy()
    df_sort.sort_values(by=col, ascending=True, inplace=True)
    df_sort.reset_index(inplace=True, drop=True)
    df_sort.reset_index(inplace=True)
    for i in range(0,len(df_sort)):
        ticker = df_sort.loc[i,'ticker']
        rank[i] = ticker
    return rank
    

def process_pool(df):
    df = basic_filter(df)
    
    pool_size = len(df)
    ranking_mark = {} # key ticker, val rank
    
    # key = col, val = ranked ticker in dict<rank, ticker>
    rank_all_col = {} 
    for col in PERF_COLS:
        rank_all_col[col] = rank_ticker_by_col(df, col)
    
    for i in range(0, pool_size):
        top_n_lists = get_0_to_n(rank_all_col, i)
        intersection = intersection_of_k_list(top_n_lists)

        
        for ticker in intersection:
            if ticker not in ranking_mark.keys():
                ranking_mark[ticker] = i
    
    # asign rank
    for i in range(0, len(df)):
        df.loc[i, 'rank'] =  ranking_mark[df.loc[i, 'ticker']]
    
    df.sort_values(by='rank', ascending=True, inplace=True)
    df.reset_index(inplace=True, drop=True)
    return df


def fetch_0_to_n_key(n, rank_dict):
    l = []
    for i in range(0, n+1):
        l.append(rank_dict[i])
    return l


def get_0_to_n(rank_all_col, n):
    top_n_lists = {}

    for col in PERF_COLS:
        top_n_lists[col] = fetch_0_to_n_key(n, rank_all_col[col])
    return list(top_n_lists.values())


def rank_stock_by_intersection():
    raw_price_files = get_all_csv_file_in_folder(TRADE_SUMMARY_ALL_TICKER)
    for file_path in raw_price_files:
        file_name = file_path.split('/')[-1]
        print('ranking: ', file_name)
        df = pd.read_csv(file_path)
        df_ranked = process_pool(df)
        output_path = ranked_ticker_path(file_name)
        df_ranked.to_csv(output_path, index=False)


def rank_stock_by_top_k_win_lose_ratio(k):
    raw_price_files = get_all_csv_file_in_folder(TRADE_SUMMARY_ALL_TICKER)
    for file_path in raw_price_files:
        file_name = file_path.split('/')[-1]
        
        df = pd.read_csv(file_path)
        df = basic_filter(df)
        df = df.nlargest(k,'win_lose_pnl_ratio')
        df.sort_values(by='win_lose_pnl_ratio', ascending=False, inplace=True)
        df.reset_index(inplace=True, drop=True)
        print('ranked: ', file_name, '  cnt:',len(df))
        output_path = ranked_ticker_path(file_name)
        df.to_csv(output_path, index=False)
        
        
# Method 1(deprecated): 
# rank_stock_by_intersection()

# Method 2
rank_stock_by_top_k_win_lose_ratio(k=100)