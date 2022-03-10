import pandas as pd
from util.util_time import df_filter_dy_date
import plotly.express as px

# path = 'D:/f_data/batch_20220214/step8_portfolio_time_series/intermediate_per_track_ticker_price.csv'
# folder_out = 'D:/f_data/batch_20220214/step8_portfolio_time_series/per_track_st_price/'
# start_date = '2008-02-27'
# end_date = '2008-03-03'

def gen_per_track_st_price_pic(
    path,
    folder_out,
    start_date,
    end_date
):
    df = pd.read_csv(path)
    df = df_filter_dy_date(df,'date',start_date,end_date)
    
    dfs = {}
    for i in range(0,50):
        print(f'plotting stock price for track {i}')
        dfs[i] = df[df['track_id']==i].copy()
        if i == 40:
            print(dfs[i])
        if (len(dfs[i]) == 0):
            print(f'no trade for track {i}')
            continue
        title = f'track_{i}'
        fig = px.line(dfs[i], x="date", y="price", color='ticker', title=title)
        
        path_out = folder_out + title + '.png'
        fig.write_image(path_out)


def gen_per_track_position_pic(
    path,
    folder_out,
    start_date,
    end_date
):
    df = pd.read_csv(path)
    df = df_filter_dy_date(df,'date',start_date,end_date)
    
    dfs = {}
    for i in range(0,50):
        print(f'plotting stock price for track {i}')
        dfs[i] = df[df['track_id']==i].copy()
#         if i == 40:
#             print(dfs[i])
        if (len(dfs[i]) == 0):
            print(f'no trade for track {i}')
            continue
        title = f'track_{i}'
        fig = px.line(dfs[i], x="date", y="roll_position", title=title)
        
        path_out = folder_out + title + '.png'
        fig.write_image(path_out)