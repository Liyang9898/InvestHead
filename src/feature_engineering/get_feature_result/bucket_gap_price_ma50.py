import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from version_master.version import (
    feature_engineering
)


def bucket(df):
    holding_days_avg= df['hold_days'].mean()
    print('holding days:', holding_days_avg)
    
    win_rate= df.groupby(by=["entry_price_ma50_gap_percent_bucket"])['win'].mean().reset_index()
    count= df.groupby(by=["entry_price_ma50_gap_percent_bucket"])['label'].count().reset_index()
    pnl_percent = df.groupby(by=["entry_price_ma50_gap_percent_bucket"])['pnl_percent'].mean().reset_index()
    
    win_df = df[df['label']==1]
    lose_df = df[df['label']==-1]
    pnl_percent_win= win_df.groupby(by=["entry_price_ma50_gap_percent_bucket"])['pnl_percent'].mean().reset_index()
    pnl_percent_lose= lose_df.groupby(by=["entry_price_ma50_gap_percent_bucket"])['pnl_percent'].mean().reset_index()
    
    holding_days_win= win_df.groupby(by=["entry_price_ma50_gap_percent_bucket"])['hold_days'].mean().reset_index()
    holding_days_lose= lose_df.groupby(by=["entry_price_ma50_gap_percent_bucket"])['hold_days'].mean().reset_index()
    
    # draw
    fig = go.Figure(data=[go.Histogram(x=df["entry_price_ma50_gap_percent_bucket"], cumulative_enabled=True,histnorm='probability density')])
    fig.show()

    fig_winrate = px.line(win_rate, x="entry_price_ma50_gap_percent_bucket", y="win", title='win rate')
    fig_winrate.show()
    fig_cnt = px.line(count, x="entry_price_ma50_gap_percent_bucket", y="label", title='case count')
    fig_cnt.show()
    
    fig_pnl = px.line(pnl_percent, x="entry_price_ma50_gap_percent_bucket", y="pnl_percent", title='pnl_percent')
    fig_pnl.show()
    
    fig_pnl_win = px.line(pnl_percent_win, x="entry_price_ma50_gap_percent_bucket", y="pnl_percent", title='pnl_percent_win')
    fig_pnl_win.show()
    
    fig_pnl_lose = px.line(pnl_percent_lose, x="entry_price_ma50_gap_percent_bucket", y="pnl_percent", title='pnl_percent_lose')
    fig_pnl_lose.show()

    hold_days_win = px.line(holding_days_win, x="entry_price_ma50_gap_percent_bucket", y="hold_days", title='hold_days_win')
    hold_days_win.show()
    
    hold_days_lose = px.line(holding_days_lose, x="entry_price_ma50_gap_percent_bucket", y="hold_days", title='hold_days_lose')
    hold_days_lose.show()
    
def main():
    path=feature_engineering+'features.csv'
    features = pd.read_csv(path)
    bucket(features)
    
    
main()