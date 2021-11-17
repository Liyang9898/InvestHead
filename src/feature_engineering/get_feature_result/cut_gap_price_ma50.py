import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from version_master.version import (
    feature_engineering
)


def bucket(df, threshold):    
    total_cnt = len(df)
    df = df[df["entry_price_ma50_gap_percent_bucket"]<threshold]
    remain_cnt = len(df)
    left = remain_cnt *1.0/total_cnt
    win_df = df[df['label']==1]
    lose_df = df[df['label']==-1]
    rate = len(win_df)/len(df)
    pnl_win = win_df['pnl_percent'].mean()
    pnl_lose = lose_df['pnl_percent'].mean()
    print('threshold:',threshold,' (',left,')', 'rate: ',rate,' win pnl:',pnl_win,' lose pnl',pnl_lose)

    
def main():
    path=feature_engineering+'features.csv'
    features = pd.read_csv(path)

    bucket(features,0.1)
    bucket(features,0.15)
    bucket(features,0.2)
    bucket(features,0.25)
    bucket(features,0.3)
    bucket(features,0.4)
    bucket(features,0.5)
    bucket(features,99999)
    
    
main()