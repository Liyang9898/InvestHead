from util.util_math import draw_x_card_out_of_y
import pandas as pd

METHOD_RANDOM = 'random'
METHOD_TOP_RETURN = 'top_return'
METHOD_TOP_WIN_RATE = 'win_rate'
METHOD_TOP_WIN_LOSE_PNL_RATIO = 'win_lose_pnl_ratio'
# METHOD_RANDOM = 'random'

def select_trades_from_available_opportunity(
    trade_opportunity,
    needed_trade_cnt,
    today_date,
    ticker_ranking_artifact,
    method,
):
    """
    select trades from all available trade opportunity
    method can be a varied
    input: 
    stock rank: ticker, other param->df
    available ticker space
    needed ticker count
    
    output:
    selected map<ticker, trades>
    """
    trades = {}
    
    if method == METHOD_RANDOM:
        trades = select_trades_random(
            trade_opportunity,
            needed_trade_cnt,
        )
    elif method == METHOD_TOP_RETURN:
        trades = select_trades_top_return(
            trade_opportunity,
            needed_trade_cnt,
            today_date,
            ticker_ranking_artifact,
        )
    elif method == METHOD_TOP_WIN_RATE:
        trades = select_trades_top_win_rate(
            trade_opportunity,
            needed_trade_cnt,
            today_date,
            ticker_ranking_artifact,
        )
    elif method == METHOD_TOP_WIN_LOSE_PNL_RATIO:
        trades = select_trades_top_win_lose_pnl_ratio(
            trade_opportunity,
            needed_trade_cnt,
            today_date,
            ticker_ranking_artifact,
        )
    
    return trades


def select_trades_random(
    trade_opportunity,
    needed_trade_cnt,
):
    """
    random pick ticker from available trade opportunities
    """
    res = {}
    opportunity_cnt = len(trade_opportunity)
    drawed_id = draw_x_card_out_of_y(needed_trade_cnt, opportunity_cnt)
    idx = 0
    for ticker, trade in trade_opportunity.items():
        # ticker not in selected_ticker_list continue
        if idx not in drawed_id:
            idx = idx + 1
            continue
        res[ticker]=trade
        idx = idx + 1
    return res


def select_trades_top_return(
    trade_opportunity,
    needed_trade_cnt,
    today_date,
    ticker_ranking_artifact,
):
    metric = 'annual_avg_return'
    res = select_trades_top_perf_metric(
        trade_opportunity,
        needed_trade_cnt,
        today_date,
        ticker_ranking_artifact,
        metric
    )
    return res


def select_trades_top_win_rate(
    trade_opportunity,
    needed_trade_cnt,
    today_date,
    ticker_ranking_artifact,
):
    metric = 'win_rate'
    res = select_trades_top_perf_metric(
        trade_opportunity,
        needed_trade_cnt,
        today_date,
        ticker_ranking_artifact,
        metric
    )
    return res


def select_trades_top_win_lose_pnl_ratio(
    trade_opportunity,
    needed_trade_cnt,
    today_date,
    ticker_ranking_artifact,
):
    metric = 'win_lose_pnl_ratio'
    res = select_trades_top_perf_metric(
        trade_opportunity,
        needed_trade_cnt,
        today_date,
        ticker_ranking_artifact,
        metric
    )
    return res


def select_trades_top_perf_metric(
    trade_opportunity,
    needed_trade_cnt,
    today_date,
    ticker_ranking_artifact,
    metric
):
    """
    pick ticker from available trade opportunities with top return
    """
    # get ranking ticker for current time period
    year = today_date.split('-')[0]
    rank_artifact_df=ticker_ranking_artifact[year].copy()
    
    # filter ranking list by trade_opportunity tickers
    # some ticker already in opened positions, some ticker does not have enter opportunity today
    d = {'ticker': list(trade_opportunity.keys())}
    trade_opportunity_df = pd.DataFrame(data=d)
    rank_artifact_df = pd.merge(rank_artifact_df, trade_opportunity_df, on="ticker")

    # filter out ranking record with too less samples
    trade_cnt_col = 'total_trades_all_entry'
    rank_artifact_df = rank_artifact_df[rank_artifact_df[trade_cnt_col] > 10].copy()
    
    # pick top ticker 
    perf_col = metric
    rank_artifact_df.sort_values(by=perf_col, ascending=False, inplace=True)
    rank_artifact_df.reset_index(inplace=True, drop=True)
    rank_artifact_df = rank_artifact_df.head(needed_trade_cnt)
    selected_ticker = rank_artifact_df['ticker'].to_list()
    
    res = {}
    for ticker, trade in trade_opportunity.items():
        # ticker not in selected_ticker_list continue
        if ticker not in selected_ticker:
            continue
        res[ticker]=trade
    return res