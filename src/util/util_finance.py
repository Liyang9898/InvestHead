from datetime import datetime
from statistics import (
    mean,
    pstdev
)

from sklearn import linear_model
from norgate.ticker_price_downloader import pull_ticker_price_locally_norgate
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from price_asset_master.lib.api.api import download_ticker
from util.general_ui import plot_line_from_xy_list, plot_lines_from_xy_list
from util.util import plot_hist_from_df_col, \
    extract_sub_df_single_st_based_on_period
from util.util_math import moving_window_pct_diff, max_pct_drop_positive_list
from util.util_time import days_gap_date_str, mark_year_month_week_start, \
    df_filter_dy_date


# from util.util_time import period_str_mark
def get_discrete_fix_roll(df):
    # input: df must have 3 column: pnl_percent, entry_ts, exit_ts
    # input assumption: all trades does not have time overlap, allow entry an exit overlap for 2 consecutive trades
    # output: df will have 4 extra column: entry_fix, exit_fix, entry_roll, exit_roll
    
    # input validation
    assert df['pnl_percent'].isnull().sum() == 0
    
    df['entry_fix'] = 1
    df['exit_fix'] = 1
    df['entry_roll'] = 1
    df['exit_roll'] = 1
    
    fix = 1
    roll = 1
    
    for i in range(0, len(df)):
          
        pnl_percent = df.loc[i, 'pnl_percent']
        fix += pnl_percent
        roll *= (1+pnl_percent)
        # set start of trade's fix and roll
        if i > 0:
            df.loc[i, 'entry_fix'] = df.loc[i-1, 'exit_fix']
            df.loc[i, 'entry_roll'] = df.loc[i-1, 'exit_roll']
            
        # set exit of trade's fix and roll
        df.loc[i, 'exit_fix'] = df.loc[i, 'entry_fix'] + pnl_percent
        df.loc[i, 'exit_roll'] = df.loc[i, 'entry_roll'] * (1 + pnl_percent)
    
    # validation
    assert fix == df.loc[len(df)-1, 'exit_fix']
    assert roll == df.loc[len(df)-1, 'exit_roll']
        

def attach_trade_max_down(df_trade, df_st):
    # input validation
    assert df_trade['pnl_percent'].isnull().sum() == 0
    
    # new output cols
    df_trade['max_down_ts'] = np.nan
    df_trade['pnl_percent_max_down'] = np.nan
    
    for i in range(0, len(df_trade)):
        
        s = df_trade.loc[i, 'entry_ts']
        e = df_trade.loc[i, 'exit_ts']
        entry_p = df_trade.loc[i, 'entry_price']
        
        # extract st price during trade
        df_st_sub = df_st[(df_st['est_datetime'] >= s) & (df_st['est_datetime'] <= e)]
        df_st_sub.reset_index(drop=True,inplace=True)
        
        max_low = entry_p
        max_low_ts = ''
        for j in range(0, len(df_st_sub)):
            p = df_st_sub.loc[j, 'low']
            if p < entry_p:
                max_low = p
                max_low_ts = df_st_sub.loc[j, 'est_datetime']
        
        df_trade.loc[i, 'max_down_ts'] = max_low_ts
        df_trade.loc[i, 'pnl_percent_max_down'] = (max_low - entry_p) / entry_p
        
        
def trade_distribution_plot(trade_path, indicator_path):
    # trade_path: csv of trades
    # indicator_path: csv of indicators
    
    # output: pnl_percent hist and max down hist
    
    df = pd.read_csv(trade_path)
    df_st = pd.read_csv(indicator_path)
    get_discrete_fix_roll(df)
    
    attach_trade_max_down(df, df_st)
    plot_hist_from_df_col(df=df, col='pnl_percent', bin_size=0.05, title='pnl_percent')
    plot_hist_from_df_col(df=df, col='pnl_percent_max_down', bin_size=0.05, title='pnl_percent_max_down')
    
    
def get_beta_from_list(baseline, target):
    array1 = np.array(baseline)
    array2 = np.array(target)
    cov_matrix = np.cov(array1, array2)
    covariance = cov_matrix[0][1]
    variance  = np.var(baseline)
    beta = covariance / variance
    return beta


def get_sharpe_ratio_from_list(prices, rf=0):
    price_series = pd.Series(prices)
    price_series = price_series.pct_change().dropna()
    mean = price_series.mean() -rf
    sigma = price_series.std()
    return mean / sigma
    
    
def moving_window_perf_bundle(positions_list, date_list, window):
#     down_data = max_drawdown_recover(positions_list, date_list)
    
    max_drawdown = max_pct_drop_positive_list(positions_list)
    down_data = {
        'max_drawdown': max_drawdown['max_drop_pct'],
        'max_recover_period': max_drawdown['max_recover_days'],
        'max_drawdown_start': date_list[max_drawdown['max_drop_pct_idx']],
        'max_recover_start': date_list[max_drawdown['max_recover_period_start']],
    }
    
    
    rets = moving_window_pct_diff(positions_list, window)
    avg_return = mean(rets)
    return_stdev = pstdev(rets)
    sharpe_ratio = avg_return / return_stdev
    max_down_sharpe_ratio = abs(avg_return / down_data['max_drawdown'])
    res = {
        'window': window,
        'avg_return': avg_return,
        'return_stdev': return_stdev,
        'max_drawdown': down_data['max_drawdown'],
        'stdev_sharpe_ratio': sharpe_ratio,
        'max_down_sharpe_ratio': max_down_sharpe_ratio
    }
    return res


def yearly_alpha(l):
    # assume l is a list of position on daily level in chronological order
    ret = l[len(l) - 1] / l[0] - 1.0
    year_cnt = len(l) / 250
    return ret / year_cnt


# position is a list of position based on day level
# this func returns the absoluta cash pnl on day level based on initial cash
def cash_pnl(positon, initial_cash):
    factor = initial_cash / positon[0]
    cash_pnl=[i*factor-initial_cash for i in positon] 
    return cash_pnl


def single_protfolio_perf(
    df, 
    date_col, 
    position_col, 
    symbol='default',
    plot_position=False,
    plot_drop_from_peak=False
):
    date_list = df[date_col].to_list()
    position_list = df[position_col].to_list()
    annual_alpha = yearly_alpha(position_list)
    drop_info_bundle = max_pct_drop_positive_list(position_list)
    
    if plot_position:
        plot_line_from_xy_list(date_list, position_list, 'position')
        
    if plot_drop_from_peak:
        plot_line_from_xy_list(date_list, drop_info_bundle['below_max_array'], 'drop array')
    
    return {
        'symbol':symbol,
        'annual_alpha':round(annual_alpha, 4),
        'max_drawdown':round(drop_info_bundle['max_drop_pct'], 4),
        'alpha_dowm_ratio':round(-annual_alpha/drop_info_bundle['max_drop_pct'], 4),
        'below_max_array': drop_info_bundle['below_max_array'],
        'date_list': date_list
    }
    
    
def multi_protfolio_perf(
    df, 
    date_col, 
    baseline_position_col, 
    exp_position_cols,
):
    #################################################################
    # we assume the initial cash of baseline is 1 dollar
    #################################################################
    initial_cash = 1
    position_map = {}
    drop_map = {}
    calibrated_pnl_map = {}
    report = {}
    report_keys = ['annual_alpha','max_drawdown','alpha_dowm_ratio']
    
    date_list = df[date_col].to_list()
    baseline_perf = single_protfolio_perf(df, date_col, baseline_position_col, 'baseline')
    position_map['baseline'] = df[baseline_position_col].to_list()
    drop_map['baseline'] = baseline_perf['below_max_array']
    baseline_maxdrop = baseline_perf['max_drawdown']
    calibrated_pnl_map['baseline'] = cash_pnl(df[baseline_position_col], initial_cash)
    report['baseline'] = { your_key: baseline_perf[your_key] for your_key in report_keys }
    
    for exp_col in exp_position_cols:
        exp_perf = single_protfolio_perf(df, date_col, exp_col, exp_col)
        position_map[exp_col] = df[exp_col].to_list()
        drop_map[exp_col] = exp_perf['below_max_array']
        
        exp_maxdrop = exp_perf['max_drawdown']
        
        # this factor means, you can do 'drop_calibrated_factor' times investment 
        # to match baseline drop 
        drop_calibrated_factor = baseline_maxdrop / exp_maxdrop
        drop_calibrated_alpha = exp_perf['annual_alpha'] * drop_calibrated_factor
        calibrated_pnl_map[exp_col] = cash_pnl(df[exp_col], initial_cash* drop_calibrated_factor)
        
        report[exp_col] = { your_key: exp_perf[your_key] for your_key in report_keys }
        report[exp_col]['drop_calibrated_alpha'] = drop_calibrated_alpha

    for k , v in report.items():
        print(k)
        print(v)
        
    plot_lines_from_xy_list(date_list, position_map, title='Position')
    plot_lines_from_xy_list(date_list, drop_map, title='Drop below previous peak')
    plot_lines_from_xy_list(date_list, calibrated_pnl_map, title='Calibrated PNL based on max drop')
    

def compute_return_compared_with_previous_row(df, date_col, position_col):
    df=df.copy()
    df['return'] = np.nan
    date_str_pre = '1000-01-01'
    pos_pre = -1
    for i in range(0, len(df)):
        # chronological order
        date_str = df.loc[i, date_col]   
        assert date_str_pre < date_str
        date_str_pre = date_str
        
        pos = df.loc[i, position_col]   
        
        # first row ignore
        if pos_pre == -1: 
            pos_pre = pos
            continue
        
        ret = pos/pos_pre-1
        pos_pre = pos
        df.loc[i, 'return'] = ret   
        
    return df


def get_return_perf(df):
    assert 'return' in df.columns
    df = df.copy()
    df.dropna(inplace=True) 
    df.reset_index(inplace=True, drop=True)

    ret_avg = df["return"].mean()
    ret_std = df["return"].std()
    ret_sharpe = ret_avg / ret_std
    
    df_win = df[df["return"]>=0]
    df_lose = df[df["return"]<0]
    assert len(df_win)+len(df_lose) == len(df)
    win_avg = df_win["return"].mean()
    lose_avg = df_lose["return"].mean()
            
    return {
        'ret_avg':round(ret_avg, 4),
        'ret_std':round(ret_std, 4),
        'ret_sharpe':round(ret_sharpe, 4),
        "positive_rate": round(len(df_win) / len(df), 4),
        'win_avg':round(win_avg, 4),
        'lose_avg':round(lose_avg, 4),
    }
    
    

def get_year_return_from_position_df(df, date_col, position_col):
    df.sort_values(by=[date_col], inplace=True)

    date_s = df.loc[0, date_col]  
    date_e = df.loc[len(df)-1, date_col]   
    duration_days = days_gap_date_str(date_s, date_e)
    duration_years = duration_days / 365
    
    close_s = df.loc[0, position_col]  
    close_e = df.loc[len(df)-1, position_col]    
    
    total_return = close_e / close_s - 1
    total_return_divide_years = total_return / duration_years
    equivalent_annual_return = (close_e / close_s) ** (1/duration_years) - 1
     
    info = {
        'total_return': total_return,
        'total_return_divide_years': total_return_divide_years,
        'equivalent_annual_return': equivalent_annual_return
    }
    return info


def get_max_drop_from_position_df(df, date_col, position_col):
    df = df.copy()
    df.sort_values(by=[date_col], inplace=True)
    
    rows = []

    # max down
    date_pre = '1000-01-01' # previous date
    max = -1 # max position
    max_below_max_pct = 0
    max_drop_date = '1000-01-01' # the date on valley
    peak_date=df.loc[0, date_col] # the day on the recent peak
    max_recover = -1
    drop_range = ''
    for i in range(0, len(df)):
        date = df.loc[i, date_col]   
        assert date > date_pre
        position = df.loc[i, position_col]       
        
        if position > max:
            # new max found
            max = position
            rows.append({'date':date,'drop_pct': 0.0})
            
            # time gap between current new peak and previous peak -> max recover
            days_gap = days_gap_date_str(peak_date, date)
            if days_gap > max_recover:
                max_recover = days_gap
                drop_range = f"{peak_date} -> {date}"
            peak_date = date
            
        else:
            # lower than previous max
            below_max_pct = position / max - 1
            rows.append({'date':date, 'drop_pct': below_max_pct})
            if below_max_pct < max_below_max_pct:
                max_below_max_pct = below_max_pct
                max_drop_date = date
    
    daily_down_df = pd.DataFrame(rows)
    info = {
        'max_below_max_pct':max_below_max_pct,
        'max_drop_date': max_drop_date,
        'daily_down_df':daily_down_df,
        'max_recover': max_recover,
        'drop_range':drop_range
    }
    return info



def get_position_perf(df, date_col, position_col):

    perf_year_return = get_year_return_from_position_df(df, date_col, position_col)
    perf_max_drop = get_max_drop_from_position_df(df, date_col, position_col)
    
    max_drop_sharpe_ratio = - perf_year_return['equivalent_annual_return'] / perf_max_drop['max_below_max_pct']
    
    info = {
        'total_return': round(perf_year_return['total_return'], 4),
        'total_return_divide_years': round(perf_year_return['total_return_divide_years'], 4),
        'compound_annual_return': round(perf_year_return['equivalent_annual_return'], 4),
        'max_below_max_pct': round(perf_max_drop['max_below_max_pct'], 4),
        'max_drop_date': perf_max_drop['max_drop_date'],
        'max_drop_sharpe_ratio': round(max_drop_sharpe_ratio, 4),
        'max_recover_days': round(perf_max_drop['max_recover'], 4),
        'drop_range': perf_max_drop['drop_range']
    }
    
    df = mark_year_month_week_start(df, date_col)
    for period in ['year', 'month', 'week']:
        df_period = extract_sub_df_single_st_based_on_period(df=df, date_col=date_col, position_col=position_col, period=period)
        df_period_return = compute_return_compared_with_previous_row(df=df_period, date_col=date_col, position_col='position')
        info[period] = get_return_perf(df_period_return)
    
    # info has a complete set of information
#     print(info)
#     print(info['max_drop_sharpe_ratio'])
    info_major_metric = {
        'ticker': 'default',
        'major_compound_annual_return': info['compound_annual_return'],
        'major_max_drop': info['max_below_max_pct'],
        'major_return_drop_ratio':info['max_drop_sharpe_ratio'],
        'major_yearly_return': info['year']['ret_avg'],
        'major_yearly_return_std': info['year']['ret_std'],
        'major_yearly_sharpe': info['year']['ret_sharpe'],
    }
    info_major_metric.update(info)
    return info_major_metric


def compute_alpha_beta_from_position(df, date_col, base_col, exp_col, period, img_path, plot=True):
    df = mark_year_month_week_start(df, date_col)

    df_period_base = extract_sub_df_single_st_based_on_period(df=df, date_col=date_col, position_col=base_col, period=period)
    df_period_base_return = compute_return_compared_with_previous_row(df=df_period_base, date_col=date_col, position_col='position')
    df_period_base_return.dropna(inplace=True)
    return_base = df_period_base_return['return'].to_list()
    
    
    df_period_exp = extract_sub_df_single_st_based_on_period(df=df, date_col=date_col, position_col=exp_col, period=period)
    df_period_exp_return = compute_return_compared_with_previous_row(df=df_period_exp, date_col=date_col, position_col='position')
    df_period_exp_return.dropna(inplace=True)
    return_exp = df_period_exp_return['return'].to_list()

    
    x = np.array(return_base).reshape(-1, 1)
    y = np.array(return_exp).reshape(-1, 1)
    
    # Create linear regression object
    regr = linear_model.LinearRegression()
    # Train the model using the training sets
    regr.fit(x, y)
    # The coefficients
    r_sq = regr.score(x, y)
    alpha = regr.intercept_[0]
    beta = regr.coef_[0][0]
    
    
    beta2 = get_beta_from_list(return_base, return_exp)
    
    
#     print('coefficient of determination:', r_sq)
#     print('intercept:', alpha)
#     print('slope:', beta)
    res = {
        'alpha':round(alpha,4),
        'beta':round(beta,4),
        'beta2':round(beta2,4),
        'r_sq':round(r_sq,4)
    }
    
    # plot chart
    if plot:
        x_list = return_base
        y_list = return_exp
        x_min = min(return_base)
        x_max = max(return_base)
        x_vals = np.arange(x_min, x_max, 0.001)
        y_vals = alpha + beta * x_vals
    
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=x_list, 
                y=y_list,
                mode='markers',
                name='return'
            )
        )
        fig.add_trace(
            go.Scatter(
                x=x_vals, 
                y=y_vals,
                mode='markers',
                name='LR'
            )
        )
        title = f'alpha={alpha} beta={beta} beta2={beta2}'
        fig.update_yaxes(
            scaleanchor = "x",
            scaleratio = 1,
            title_text='experiment return'
        )
        fig.update_xaxes(title_text='baseline return')
        fig.update_layout(title=title)
        # save image to file
        fig.write_image(img_path)
 
        
#         
#         plt.scatter(x, y,  color='black')
#          
#         axes = plt.gca()
#         x_vals = np.array(axes.get_xlim())
#         y_vals = alpha + beta * x_vals
#         plt.plot(x_vals, y_vals, '--')
#         plt.title("Return LR")
#         plt.xlabel("Baseline return")
#         plt.ylabel("Experiment return")
#         plt.grid()
#         plt.show()

    return res
    

# give a df with date_col and position col
# compute the speed in time bucket, if bucket = 1, the speed = this (row-previous_row)/1
def get_line_speed(df, date_col, position_col, time_bucket, path=None):
    df.sort_values(by=[date_col], inplace=True)
    df_new = df[[date_col]].copy()
    df_new['velocity'] = np.nan
    for i in range(0, len(df) - time_bucket):
        s = i
        e = i + time_bucket
#         date =  df.loc[s, date_col] 
        p_s = df.loc[s, position_col] 
        p_e = df.loc[e, position_col] 
        v = (p_e/p_s-1) / time_bucket
#         print(date, p_s,p_e,v)
        df_new.loc[e, 'velocity'] = v
    return df_new
  

def get_line_speed_chart(df, date_col, baseline_col, position_col, time_bucket, path=None):
    df_base = get_line_speed(df, date_col, baseline_col, time_bucket)
    df_base.rename(columns={'velocity':'velocity_base'},inplace=True)
    df_exp = get_line_speed(df, date_col, position_col, time_bucket)
    df_exp.rename(columns={'velocity':'velocity_exp'},inplace=True)
    df_new = pd.merge(df_base, df_exp, on='date')
    if path is not None:
        path = path + 'speed.png'
    plot_lines_from_xy_list(
        x_list=df_new['date'].to_list(), 
        y_list_map={'base': df_new['velocity_base'].to_list(),'exp': df_new['velocity_exp'].to_list()}, 
        title=f'velocity time_bucket={time_bucket}',
        path=path
    )
    

def perf_vs_benchmark(
    baseline_ticker,
    experiment_ticker,
    start_date,
    end_date,
    result_folder
):
    return


def compuate_alpha_beta_to_csv_img(
    position_csv, 
    date_col, 
    position_col, 
    start_date, 
    end_date, 
    benchmark_ticker,
    period,
    result_path,
    norgate
):
    """
    period: year, month, week
    """
    result_path_csv = f'{result_path}{period}_alpha_beta.csv'
    result_path_img = f'{result_path}{period}_alpha_beta.png'
    
    # prepare benchmark
    interval = '1d'
    path = 'D:/f_data/temp/temp_benchmark.csv'
#     download_ticker(benchmark_ticker, start_date, end_date, path, interval)
#     api_download_ticker(benchmark_ticker, start_date, end_date, path, interval, norgate)

    if not norgate:
        download_ticker(benchmark_ticker, start_date, end_date, path, interval)
    else:
        pull_ticker_price_locally_norgate(benchmark_ticker, start_date, end_date, path)
        
    
    df = pd.read_csv(path)
    df['date']=df.apply(lambda row : str(datetime.fromtimestamp(int(row['unixtime'])).strftime('%Y-%m-%d')), axis = 1)
    df['benchmark'] = df['Close']
    
    # process position
    df_pos = pd.read_csv(position_csv)
    df_pos['date'] = df_pos[date_col]
    df_pos_filtered = df_filter_dy_date(df_pos,'date',start_date,end_date)
    
    # merge all results
    merged_df = pd.merge(df_pos_filtered, df, how="inner", on="date")
    alpha_beta = compute_alpha_beta_from_position(merged_df, 'date', 'benchmark', position_col, period, result_path_img)
    df_ab = pd.DataFrame([alpha_beta])
    df_ab.to_csv(result_path_csv, index=False)
    
    
def get_trade_perf_from_trades_csv(trades_csv, output_perf_csv):
    df = pd.read_csv(trades_csv)
    df_complete = df[df['complete']==True]
    df_win = df_complete[df_complete['pnl_percent'] > 0]
    df_lose = df_complete[df_complete['pnl_percent'] < 0]
    
    total_trade = len(df_complete)
    win_cnt = len(df_win)
    lose_cnt = len(df_lose)
    
    win_pnl_avg = df_win['pnl_percent'].mean()
    lose_pnl_avg = df_lose['pnl_percent'].mean()
    win_rate = win_cnt / total_trade
    lose_rate = lose_cnt / total_trade
    
    win_lose_pnl_ratio = (win_rate * win_pnl_avg) / (lose_rate * lose_pnl_avg) * -1
    
    stat = {
        'ticker': 'portfolio',
        'win_rate':round(win_rate,4),
        'lose_rate':round(lose_rate,4),
        'win_pnl_avg':round(win_pnl_avg,4),
        'lose_pnl_avg':round(lose_pnl_avg,4),
        'win_lose_pnl_ratio':round(win_lose_pnl_ratio,4),
        'total_trades':round(total_trade,4),
    }
    df_stat = pd.DataFrame([stat])
    df_stat.to_csv(output_perf_csv, index=False)
    
    
