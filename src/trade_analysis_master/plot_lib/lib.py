from datetime import datetime, timedelta
# from plotly.validators.streamtube import starts
import plotly.graph_objects as go

def time_range_gain(df, diff, ticker):
    # validation
    for i in range(0, len(df)-1):
        assert df.loc[i, 'date'] < df.loc[i+1, 'date']
    
    # real job
    res = {}
    cur_s = 0
    while cur_s <= len(df)-1:
        cur_e = cur_s + diff - 1
        if cur_e > len(df)-1:
            cur_e = len(df)-1
        dt = df.loc[cur_s, 'date']
        pos_s = df.loc[cur_s, ticker]
        pos_e = df.loc[cur_e, ticker]
        val = pos_e/pos_s-1
        res[dt] = val
        cur_s = cur_s + diff
    return res

def list_delta(exp,base):
    assert len(exp)==len(base)
    res = []
    for i in range(0, len(exp)): 
        res.append(exp[i]-base[i])
    return res

def incremental(l):
    res = [] 
    res.append(1)
    for x in l:
        y = res[len(res)-1] + x
        res.append(y)
    return res

def roll(l):
    res = [] 
    res.append(1)
    for x in l:
        y = res[len(res)-1] * (1+x)
        res.append(y)
    return res


def ab_test(df_merge, exp_ticker, base_ticker, diff):
    base = time_range_gain(df=df_merge, diff=diff, ticker=base_ticker)
    exp = time_range_gain(df=df_merge, diff=diff, ticker=exp_ticker)
    
    
    fig_compare = go.Figure()
    exp_base_delta = list_delta(list(exp.values()),list(base.values()))
    cnt = 0
    positive = 0
    for x in exp_base_delta:
        cnt += 1
        if x > 0:
            positive += 1
    out_perform_rate = positive *1.0 / cnt
    fig_compare_title = 'AB test, out perform rate:' + str(out_perform_rate)
    
    fig_compare.add_trace(go.Bar(x=list(base.keys()), y=list(base.values()),name='Base: '+base_ticker))
    fig_compare.add_trace(go.Bar(x=list(exp.keys()), y=list(exp.values()),name='Exp: '+exp_ticker))
    fig_compare.add_trace(go.Bar(x=list(exp.keys()), y=exp_base_delta,name='diff'))
    fig_compare.update_layout(title=fig_compare_title,xaxis_title='Time',yaxis_title='Gain %')
    fig_compare.show()
    
    fig_normalized = go.Figure()
    ab_inc = incremental(exp_base_delta)
    ab_roll = roll(exp_base_delta)
    fig_normalized.add_trace(go.Scatter(x=list(base.keys()), y=ab_inc,mode='lines',name='incremental'))
    fig_normalized.add_trace(go.Scatter(x=list(exp.keys()), y=ab_roll,mode='lines',name='roll'))
    fig_normalized.update_layout(title='AB test aggregated',xaxis_title='Time',yaxis_title='Gain %')
    fig_normalized.show()
    
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Histogram(histnorm='percent',x=list(base.values()),name='Base: '+base_ticker))
    fig_hist.add_trace(go.Histogram(histnorm='percent',x=list(exp.values()),name='Exp: '+exp_ticker))
    fig_hist.add_trace(go.Histogram(histnorm='percent',x=exp_base_delta,name='Normalized on base'))
    fig_hist.update_layout(title='AB test profit distribution',xaxis_title_text='Gain %',yaxis_title_text='percent')
    fig_hist.show()