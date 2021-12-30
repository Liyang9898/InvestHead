import pandas as pd
import plotly.graph_objects as go
from util.general_ui import plot_lines_from_xy_list, plot_bars_from_xy_list
from util.util import extract_sub_df_single_st_based_on_period
from util.util_finance import get_max_drop_from_position_df, \
    compute_return_compared_with_previous_row
from util.util_pandas import df_normalize, df_multiply_factor
from util.util_time import mark_year_month_week_start


def get_drop_chart(df, date_col, base_col, exp_col, path=None):
    drop_df_base = get_max_drop_from_position_df(df, date_col, base_col)['daily_down_df']
    drop_df_base.rename(columns={'drop_pct':'drop_pct_base'},inplace=True)
    drop_df_exp = get_max_drop_from_position_df(df, date_col, exp_col)['daily_down_df']
    drop_df_exp.rename(columns={'drop_pct':'drop_pct_exp'},inplace=True)
    drop_df = pd.merge(drop_df_base, drop_df_exp, how="outer", on=date_col)
    
    x_list = drop_df['date'].to_list()
    y_list_map = {
        'drop_pct_base':drop_df['drop_pct_base'].to_list(),
        'drop_pct_exp':drop_df['drop_pct_exp'].to_list(),
    }
    if path is not None:
        path = path + 'drop_chart.png'

    plot_lines_from_xy_list(x_list, y_list_map, title='Drop from max',path=path)



def get_return_chart_period(df, date_col, base_col, exp_col, period, path=None):
    df = mark_year_month_week_start(df, date_col)

    df_period_base = extract_sub_df_single_st_based_on_period(df=df, date_col=date_col, position_col=base_col, period=period)
    df_period_base_return = compute_return_compared_with_previous_row(df=df_period_base, date_col=date_col, position_col='position')
    df_period_base_return.rename(columns={'return':'return_baseline'},inplace=True)
    
    df_period_exp = extract_sub_df_single_st_based_on_period(df=df, date_col=date_col, position_col=exp_col, period=period)
    df_period_exp_return = compute_return_compared_with_previous_row(df=df_period_exp, date_col=date_col, position_col='position')
    df_period_exp_return.rename(columns={'return':'return_experiment'},inplace=True)

    return_df = pd.merge(df_period_base_return, df_period_exp_return, how="outer", on=date_col)

    
    x_list = return_df['date'].to_list()
    y_list_map = {
        'return_baseline':return_df['return_baseline'].to_list(),
        'return_experiment':return_df['return_experiment'].to_list(),
    }
    if path is not None:
        path = path + period + '_return.png'
    plot_lines_from_xy_list(x_list, y_list_map, title=period + ' return',path=path)
    

def get_return_chart_delta_period(df, date_col, base_col, exp_col, period, path=None):
    df = mark_year_month_week_start(df, date_col)

    df_period_base = extract_sub_df_single_st_based_on_period(df=df, date_col=date_col, position_col=base_col, period=period)
    df_period_base_return = compute_return_compared_with_previous_row(df=df_period_base, date_col=date_col, position_col='position')
    df_period_base_return.rename(columns={'return':'return_baseline'},inplace=True)
    
    df_period_exp = extract_sub_df_single_st_based_on_period(df=df, date_col=date_col, position_col=exp_col, period=period)
    df_period_exp_return = compute_return_compared_with_previous_row(df=df_period_exp, date_col=date_col, position_col='position')
    df_period_exp_return.rename(columns={'return':'return_experiment'},inplace=True)

    return_df = pd.merge(df_period_base_return, df_period_exp_return, how="outer", on=date_col)

    base_list = return_df['return_baseline'].to_list()
    exp_list = return_df['return_experiment'].to_list()
    delta_list = []
    for i in range(0,len(base_list)):
        delta_list.append(exp_list[i]-base_list[i])
    
    x_list = return_df['date'].to_list()
    y_list = delta_list
    
    cnt = 0
    sum = 0
    for x in delta_list:
        if x > 0:
            cnt = cnt + 1
            sum = sum + x
            
    out_perform_rate = round(cnt/len(delta_list),4)
    avg = round(sum/len(delta_list),4) 
    if path is not None:
        path = path + period + '_return_delta.png'
    plot_bars_from_xy_list(
        x_list, 
        y_list, 
        title=period + f' return, dalta out_perform_rate:{out_perform_rate} avg = {avg}',
        path=path
    )
    
 
    
def plot_candle_stick_with_trace(
    df, 
    traces,
    title='default'
):

    price_traces =go.Candlestick(
        x=df['est_datetime'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
    )
    
    trace_ema8={
        "mode": "lines", 
        "name": "ema8", 
        "type": "scatter", 
        "x":df['est_datetime'],
        "y":df['ema8'],
        "line_color":"royalblue",
        "line":{
            "width":1
        }
    }
    
    trace_ema21={
        "mode": "lines", 
        "name": "ema21", 
        "type": "scatter", 
        "x":df['est_datetime'],
        "y":df['ema21'],
        "line_color":"orange",
        "line":{
            "width":1
        }
    }
    
    trace_ma50={
        "mode": "lines", 
        "name": "ma50", 
        "type": "scatter", 
        "x":df['est_datetime'],
        "y":df['ma50'],
        "line_color":"red",
        "line":{
            "width":1
        }
    }


    trace = [
        price_traces,
        trace_ema8, 
        trace_ema21, 
        trace_ma50,
    ]
    
    for name, t in traces.items():
        trace_enter={
            "mode": "markers", 
            "name": name, 
            "type": "scatter", 
            "x":t["x"],
            "y":t["y"],
            "line_color":"purple",
            "line":{
                "width":1
            }
        }
        trace.append(trace_enter)

    fig = go.Figure(data=trace)
    fig.update_layout(title_text=title)
    fig.show()


def plot_chart_from_df(df_pos, date_col, base_col, experiment_col, path=None):
    df = df_pos.copy()
    df.sort_values(by=[date_col], inplace=True)
    df.reset_index(inplace=True, drop=True)

    if path is not None:
        path = path = path + 'df.png'
    plot_lines_from_xy_list(
        x_list=df['date'].to_list(), 
        y_list_map={
            base_col:df[base_col].to_list(),
            experiment_col:df[experiment_col].to_list()
        }, 
        title='dataframe',
        path = path
    )
 
    
def plot_chart_normalized_on_start(df_pos, date_col, base_col, experiment_col, path=None):
    df = df_pos.copy()
    df.sort_values(by=[date_col], inplace=True)
    df.reset_index(inplace=True, drop=True)
    df_normalize(df=df, normalize_col=base_col)
    df_normalize(df=df, normalize_col=experiment_col)
    if path is not None:
        path = path = path + 'normalized_on_start.png'
    plot_lines_from_xy_list(
        x_list=df['date'].to_list(), 
        y_list_map={
            base_col:df[base_col].to_list(),
            experiment_col:df[experiment_col].to_list()
        }, 
        title='Position Normalized',
        path = path
    )
    
    
def plot_chart_normalized_on_abs_return(df_pos, date_col, base_col, experiment_col, path=None):
    df = df_pos.copy()
    df.sort_values(by=[date_col], inplace=True)
    df.reset_index(inplace=True, drop=True)
    base_return = df.loc[len(df)-1, base_col] / df.loc[0, base_col] - 1
    exp_return = df.loc[len(df)-1, experiment_col] / df.loc[0, experiment_col] - 1
    
    base_start_pos = 1
    exp_start_pos = base_start_pos*base_return/exp_return
    
    df_normalize(df=df, normalize_col=base_col)
    df_multiply_factor(df, experiment_col, exp_start_pos / df.loc[0, experiment_col])
    
    df[base_col] = df[base_col] - df.loc[0, base_col]
    df[experiment_col] = df[experiment_col] - df.loc[0, experiment_col]
    
    exp_start_pos_round = round(exp_start_pos, 2)
    if path is not None:
        path = path = path + 'normalized_on_abs_return.png'
    plot_lines_from_xy_list(
        x_list=df['date'].to_list(), 
        y_list_map={
            base_col:df[base_col].to_list(),
            experiment_col:df[experiment_col].to_list()
        }, 
        title=f'Absolute Return Align, baseline initial={base_start_pos}, exp initial={exp_start_pos_round}',
        path=path 
    )
