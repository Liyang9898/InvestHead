import plotly.graph_objects as go
from util.util import plotly_color


def ploty_stock_option(df, normalize=True):
    if len(df) == 0:
        return 
    ticker = df.loc[0, 'ticker']
    
    st_base = df.loc[0, 'stock_price']
    op_base = df.loc[0, 'option_price']

    df['stock_price_normalize'] = df['stock_price'] / st_base
    df['option_price_normalize'] = df['option_price'] / op_base
    
    fig = go.Figure()
    y1 = 'stock_price'
    y2 = 'option_price'
    if normalize:
        y1 = 'stock_price_normalize'
        y2 = 'option_price_normalize'
    fig.add_trace(go.Scatter(x=df['date'], y=df[y1],
                        mode='lines+markers',
                        name=y1))
    fig.add_trace(go.Scatter(x=df['date'], y=df[y2],
                        mode='lines+markers',
                        name=y2))
    fig.update_layout(title=f"{ticker} stock option price")
    fig.show()
    

def ploty_leverage(df, absolute=True):
    ticker = df.loc[0, 'ticker']
    y1 = 'leverage'
    t= 'leverage_yesterday'
    if absolute:
        y1 = 'leverage_ab'
        t = 'leverage absolute'
    title = f"{ticker}  {t}"
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['date'], y=df[y1],
        mode='lines+markers',
        name=y1
    ))
    fig.update_layout(title=title)
    fig.show()
    
    

def ploty_stock_option_batch(dfs, normalize=True):
    fig = go.Figure()
    colors = plotly_color()
    id = 0
    for tag, df in dfs.items():
        if len(df) == 0:
            return 
        ticker = df.loc[0, 'ticker']
        
        st_base = df.loc[0, 'stock_price']
        op_base = df.loc[0, 'option_price']
    
        df['stock_price_normalize'] = df['stock_price'] / st_base
        df['option_price_normalize'] = df['option_price'] / op_base
        
        
        y1 = 'stock_price'
        y2 = 'option_price'
        if normalize:
            y1 = 'stock_price_normalize'
            y2 = 'option_price_normalize'
        fig.add_trace(go.Scatter(x=df['date'], y=df[y1],
                            mode='lines',
                            line = dict(dash='dash', color=colors[id]),
                            name=f"{tag} stock"))
        fig.add_trace(go.Scatter(x=df['date'], y=df[y2],
                            mode='lines+markers',
                            name=f"{tag} option",
                            line = dict(color=colors[id]),
                            marker_symbol='x-open-dot'))
        id += 1
    fig.update_layout(title=f"{ticker} stock option price")
    fig.show()
    
    
def ploty_leverage_batch(dfs, absolute=True):
    fig = go.Figure()
    for tag, df in dfs.items():
        ticker = df.loc[0, 'ticker']
        y1 = 'leverage'
        t= 'leverage_yesterday'
        if absolute:
            y1 = 'leverage_ab'
            t = 'leverage absolute'
        title = f"{ticker}  {t}"
        
        fig.add_trace(go.Scatter(
            x=df['date'], y=df[y1],
            mode='lines+markers',
            name=tag
        ))
    fig.update_layout(title=title)
    fig.show()