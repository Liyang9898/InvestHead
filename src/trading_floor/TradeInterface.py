'''
Created on Jun 7, 2020

@author: leon
'''
from numpy import average
from pandas._libs import index

from global_constant.constant import folder_path_trade_ml_sample, trade_feature
from indicator_master.constant import trade_summary_interface
import pandas as pd
from plotting_lib.simple import plotTimeSerisDic, plotTimeSerisDic3
from util import util
from util.util_time import days_gap_date_str


# import plotly.express as px
# from builtins import None
# from trade_analysis_lib._all_sweep_result_analysis import total_rate
class Trade:
    TRADE_SCHEMA = [
        "entry_price",
        "entry_ts",
        "exit_price",
        "exit_ts",
        "direction",
        "bar_duration",
        "pnl",
        "pnl_percent",
        "best_potential_pnl_percent",
        "complete"
    ]
    
    def __init__(self, entry_price, entry_ts, exit_price, exit_ts, direction, bar_duration,best_potential_pnl_percent,complete=True):
        self.entry_price = entry_price
        self.entry_ts = entry_ts
        self.exit_price = exit_price
        self.exit_ts = exit_ts
        self.direction = direction
        self.bar_duration = bar_duration
        self.pnl = (exit_price - entry_price) * direction
        self.pnl_percent = self.pnl / entry_price
        self.best_potential_pnl_percent = best_potential_pnl_percent
        self.complete=complete
        self.ml_sample={'valid':0}

    
    def trade2dic(self):
        res = {
            'entry_price':self.entry_price,
            'entry_ts':self.entry_ts,
            'exit_price':self.exit_price,
            'exit_ts':self.exit_ts,
            'direction':self.direction,
            'bar_duration':self.bar_duration,
            'pnl':self.pnl,
            'pnl_percent':self.pnl_percent,
            'best_potential_pnl_percent':self.best_potential_pnl_percent,
            'complete': self.complete
        }
#         print(res.keys())
#         print(self.TRADE_SCHEMA)
        assert list(res.keys()) == self.TRADE_SCHEMA
        return res
    
    def print_trade(self):
        trade_str=util.print_trade(
            self.pnl,
            self.pnl_percent,
            self.direction,
            self.bar_duration,
            self.entry_price,
            self.entry_ts,
            self.exit_price,
            self.exit_ts,
            self.best_potential_pnl_percent
        )
        print(trade_str)
    
    
    # for ML analysis purpose
    def gen_trade_ml_sample(
        self,
        ema_8_v_yesterday,
        ema_21_v_yesterday,
        ema_8_21_gap_yesterday,
        ema_8_strict_sequence_yesterday,
        pnl_p_per_trade,
        entry_time
    ):
        if not self.complete:
            return
        self.ml_sample['valid'] = 1
        self.ml_sample['label'] = 0
        if self.pnl > 0:
            self.ml_sample['label'] = 1
        elif self.pnl < 0:
            self.ml_sample['label'] = -1
        else:
            self.ml_sample['label'] = 0
            
        self.ml_sample['ema_8_v_yesterday'] = ema_8_v_yesterday
        self.ml_sample['ema_21_v_yesterday'] = ema_21_v_yesterday
        self.ml_sample['ema_8_21_gap_yesterday'] = ema_8_21_gap_yesterday
        self.ml_sample['ema_8_strict_sequence_yesterday'] = ema_8_strict_sequence_yesterday
        self.ml_sample['pnl_p_per_trade'] = pnl_p_per_trade
        self.ml_sample['entry_time'] = entry_time
        

#         result = "Win" 
#         if self.pnl < 0:
#             result = "Lose"
#         elif self.pnl == 0:
#             result = "Neutral"
#             
#         direction_str = "Long" if self.direction == 1 else "Short"
#         trade_str="{result}, {direction_str}, {pnl_percent}({pnl}), {duration} bars,     in:{entry_price} ({entry_ts})   out:{exit_price} ({exit_ts})  best pnl%:{best_pnl_p}".format(
#             result=result,
#             direction_str=direction_str,
#             pnl_percent="{:.2%}".format(self.pnl_percent),
#             pnl=str(round(self.pnl, 2)),
#             duration=self.bar_duration,
#             entry_price=str(round(self.entry_price, 2)),
#             entry_ts=self.entry_ts,
#             exit_price=str(round(self.exit_price, 2)),
#             exit_ts=self.exit_ts,
#             best_pnl_p="{:.2%}".format(self.best_potential_pnl_percent),
#         )
#         print(trade_str)
        
class TradeBundle:
#     necessary trade summary
#     trade count: win, lose, neutual, total
#     rate: win rate, lose rate, neutral rate, win-lose rate
#     pnl_absolute: win, lose, total
#     pnl_percent:win,lose, total_fixed_agg, total_rollover
#     bar count
    def __init__(self):
        self.strategy_params={}
        self.trades=[]
        self.win_trades=[]
        self.lose_trades=[]
        self.neutral_trades=[]
        
        #     trade count
        self.win = 0
        self.lose = 0
        self.neutral = 0
        self.total_trades = 0
        
        # rate
        self.win_rate=0.0
        self.lose_rate=0.0
        self.neutral_rate=0.0
        self.win_lose_diff_rate=0.0
        
        #     pnl_absolute
        self.win_pnl = 0
        self.lose_pnl = 0
        self.total_pnl = 0
        
        #     pnl_percent
        self.win_pnl_p = 0
        self.lose_pnl_p = 0
        self.total_pnl_fixed = 0
        self.roll_over_pnl_p = 1 # this is the position, not position change
        
        self.bar_count = 0
        
        #plot data
        self.win_entry_plots = {}
        self.win_exit_plots = {}
        self.lose_entry_plots = {}
        self.lose_exit_plots = {}
        self.neutral_entry_plots = {}
        self.neutral_exit_plots = {}
        
        # PNL size
        self.win_average_pnl = 0
        self.lose_average_pnl = 0
        
        # other stats
        self.win_lose_pnl_ratio = 0
        
        # time
        self.start_time = '9999-01-01'
        self.end_time = '1000-01-01'
        

    def setBarCount(self, count):
        self.bar_count = count

    def setStrategyParams(self, params):
        self.strategy_params=params

    def addTrade(self, trade):
        self.trades.append(trade)
        
    def genTradesSummary(self):
        
        for trade in self.trades:
            if trade.entry_ts < self.start_time:
                self.start_time = trade.entry_ts
            if trade.exit_ts > self.end_time:
                self.end_time = trade.exit_ts
            
            if trade.pnl>0:
                self.win = self.win + 1
                self.win_pnl = self.win_pnl + trade.pnl
                self.win_pnl_p = self.win_pnl_p + trade.pnl_percent
                self.roll_over_pnl_p = self.roll_over_pnl_p * (1+trade.pnl_percent)
            elif trade.pnl<0:
                self.lose = self.lose + 1
                self.lose_pnl = self.lose_pnl + trade.pnl
                self.lose_pnl_p = self.lose_pnl_p + trade.pnl_percent
                self.roll_over_pnl_p = self.roll_over_pnl_p * (1+trade.pnl_percent)
            else:
                self.neutral = self.neutral + 1

        self.total_trades = self.win+self.lose+self.neutral
        
        if self.total_trades > 0:
            self.win_rate = self.win/self.total_trades
            self.lose_rate = self.lose/self.total_trades
            self.neutral_rate = self.neutral/self.total_trades
            
        if self.win != 0:
            self.win_average_pnl = self.win_pnl_p / self.win
        if self.lose != 0:
            self.lose_average_pnl = self.lose_pnl_p / self.lose
            
        for trade in self.trades:
            if trade.pnl>0:
                self.win_trades.append(trade)
            elif trade.pnl<0:
                self.lose_trades.append(trade)
            else:
                self.neutral_trades.append(trade)   
                
        self.win_lose_diff_rate=self.win_rate-self.lose_rate
        self.total_pnl = self.win_pnl+self.lose_pnl
        self.total_pnl_fixed = self.win_pnl_p + self.lose_pnl_p
        
        if self.lose_pnl == 0 and self.win_pnl == 0:
            self.win_lose_pnl_ratio = 0
        elif self.lose_pnl == 0 and self.win_pnl > 0: 
            self.win_lose_pnl_ratio = 0
        elif self.lose_pnl > 0:
            self.win_lose_pnl_ratio = self.win_pnl / self.lose_pnl * -1

        
        
    def printTradesSummary(self):
        trade_summary_str = util.printTradesSummary(
            self.win_rate,
            self.lose_rate,
            self.neutral_rate,
            self.total_trades,
            self.bar_count,
            self.win,
            self.win_pnl,
            self.win_pnl_p,
            self.lose,
            self.lose_pnl,
            self.lose_pnl_p,
            self.neutral,
            self.roll_over_pnl_p,
            self.total_pnl,
            self.win_average_pnl,
            self.lose_average_pnl,
            self.win_lose_pnl_ratio,
            self.strategy_params
        )
        print(trade_summary_str)

        
    def tradeSummary2dict(self):
        d = {
            'win_rate': [self.win_rate], 
            'lose_rate': [self.lose_rate],
            'neutral_rate': [self.neutral_rate],
            'total_rate': [self.win_rate-self.lose_rate],

            'win': [self.win],
            'lose': [self.lose],
            'neutral': [self.neutral],
            
            
            'win_pnl_p': [self.win_pnl_p],
            'lose_pnl_p': [self.lose_pnl_p],
            'total_pnl_fix':[self.total_pnl_fixed],
            'total_pnl_rollover':[self.roll_over_pnl_p],
            
            
            'bar_count':[self.bar_count],
            'total_trades': [self.total_trades],
            'trading_params': [util.encode_dict(self.strategy_params)],
            
            'start_time': self.start_time,
            'end_time': self.end_time,
        }
        return d

        
    def tradeSummary2CSV(self, path_out):
        d = self.tradeSummary2dict()
        df = pd.DataFrame(data=d)
        df.to_csv(path_out)
        print('write to:',path_out)

        
    def trades2CSV(self, path_out):
        trade_dic_list = []
        for trade in self.trades: # it's possible that there is no trades and we won't enter this loop
            trade_dic = trade.trade2dic()
            trade_dic_list.append(trade_dic)
            
        trades_df = pd.DataFrame(columns=Trade.TRADE_SCHEMA)
        if len(trade_dic_list) != 0:
            trades_df = pd.DataFrame(trade_dic_list)
        trades_df.to_csv(path_out, index=False)
    
    
    def printWinTrades(self):
        for trade in self.win_trades:
            trade.print_trade()
                
    def printLoseTrades(self):
        for trade in self.lose_trades:
            trade.print_trade()

    def printNeutralTrades(self):
        for trade in self.neutral_trades:
            trade.print_trade()
            
    
    # plotting util function
    def genPlotDataMap(self, trades, is_entry):
        # trades are one of win, lose or neutral
        map_data = {}
        for trade in trades:
            if is_entry:
                x=trade.entry_ts
                y=trade.entry_price
            else:
                x=trade.exit_ts
                y=trade.exit_price
            map_data[x]=y
        return map_data
    
    def genAllPlotDataMap(self):
        self.win_entry_plots = self.genPlotDataMap(self.win_trades, True)
        self.win_exit_plots = self.genPlotDataMap(self.win_trades, False)
        self.lose_entry_plots = self.genPlotDataMap(self.lose_trades, True)
        self.lose_exit_plots = self.genPlotDataMap(self.lose_trades, False)
        self.neutral_entry_plots = self.genPlotDataMap(self.neutral_trades, True)
        self.neutral_exit_plots = self.genPlotDataMap(self.neutral_trades, False)
        
    def genMLSample2CSV(self, file_name):
        df_list=[]
        for trade in self.trades:
            sample = trade.ml_sample
            if sample['valid'] == 0:
                continue
            util.bracket_value_in_dict(sample)
            trade_sample_df = pd.DataFrame(data=sample)
            df_list.append(trade_sample_df)
        merged = pd.concat(df_list)
        path_out = folder_path_trade_ml_sample+file_name+".csv"
        merged.to_csv(
            path_out, 
            columns =trade_feature,# must match d
            index=False
        )
        print('Written ML sample to:',path_out)


#     def trading_bundle_2_csv(self, csv_path):
#         rows = []
#         
#         for trade in self.trades:
#             row = trade.trade2dic()
#             rows.append(row)
#         df = pd.DataFrame(rows)
#         df.to_csv(csv_path, index=False)

def genTradingBundleFromCSV(path):
    df = None
    try:
        df = pd.read_csv(path)
    except:
        return None
    trades = genTradingBundleFromDataframe(df)   
    return trades


def genTradingBundleFromDataframe(df):
    trades = TradeBundle()
    for i in range(0, len(df)):
        trade = Trade(
            entry_price=df.loc[i, 'entry_price'], 
            entry_ts=df.loc[i, 'entry_ts'], 
            exit_price=df.loc[i, 'exit_price'], 
            exit_ts=df.loc[i, 'exit_ts'], 
            direction=df.loc[i, 'direction'], 
            bar_duration=df.loc[i, 'bar_duration'],
            best_potential_pnl_percent=df.loc[i, 'best_potential_pnl_percent'],
            complete=df.loc[i, 'complete']
        )
        trades.addTrade(trade)
    trades.genTradesSummary()    
    return trades
       

def genTradeBundleFromTradesList(trades, strategy):
    tradeBundle = TradeBundle()
    tradeBundle.setStrategyParams(strategy.getStrategyParams())
    for trade in trades:
        tradeBundle.addTrade(trade)
    tradeBundle.genTradesSummary()
    return tradeBundle

def merge_trade_summary(consecutive, all_entry):
    average_trade_win_pnl_p=0
    average_trade_lose_pnl_p=0
    if all_entry['win'][0] !=0:
        average_trade_win_pnl_p= all_entry['win_pnl_p'][0]/all_entry['win'][0]
    if all_entry['lose'][0] !=0:
        average_trade_lose_pnl_p= all_entry['lose_pnl_p'][0]/all_entry['lose'][0]
    each_trade_win_lose_rate=0 
    if average_trade_lose_pnl_p:
        each_trade_win_lose_rate = average_trade_win_pnl_p/average_trade_lose_pnl_p*-1
        
        
    win_factor = all_entry['win_rate'][0] * average_trade_win_pnl_p
    lose_factor = all_entry['lose_rate'][0] * average_trade_lose_pnl_p
    
    if win_factor == 0 and lose_factor == 0:
        win_lose_pnl_ratio = 0
    elif win_factor > 0 and lose_factor == 0:
        win_lose_pnl_ratio = 9999
    elif lose_factor != 0 :
        win_lose_pnl_ratio = win_factor / lose_factor * -1
    
    start_time = all_entry['start_time'] # ex:2020-01-07 00:00:00
    end_time = all_entry['end_time']
    start_date = start_time.split(' ')[0]
    end_date = end_time.split(' ')[0]
    
    days = days_gap_date_str(start_date, end_date)
    years = days / 365
    anual_return_avg = pow((consecutive['total_pnl_fix'][0]+1), 1/years)-1
    
    d = {
        'win_rate': consecutive['win_rate'][0], 
        'lose_rate': consecutive['lose_rate'][0],
        'neutral_rate': consecutive['neutral_rate'][0],
        'total_rate': consecutive['total_rate'][0],
        
        # count
        'win': consecutive['win'][0],
        'lose': consecutive['lose'][0],
        'neutral': consecutive['neutral'][0],
        
        
        'win_pnl_p': consecutive['win_pnl_p'][0],
        'lose_pnl_p': consecutive['lose_pnl_p'][0],
        'total_pnl_fix':consecutive['total_pnl_fix'][0],
        'total_pnl_rollover':consecutive['total_pnl_rollover'][0],
        
        
        'bar_count':consecutive['bar_count'][0],
        'total_trades': consecutive['total_trades'][0],
        'trading_params': consecutive['trading_params'][0],
        

        # parallel universe
        'all_universe_win_rate': all_entry['win_rate'][0], 
        'all_universe_lose_rate': all_entry['lose_rate'][0],
        'all_universe_neutral_rate': all_entry['neutral_rate'][0],
        'all_universe_total_rate': all_entry['total_rate'][0],
        
        'all_universe_win_pnl_p': all_entry['win_pnl_p'][0],
        'all_universe_lose_pnl_p': all_entry['lose_pnl_p'][0],
        'all_universe_total_trades': all_entry['total_trades'][0],
        
        'average_trade_win_pnl_p': average_trade_win_pnl_p,
        'average_trade_lose_pnl_p': average_trade_lose_pnl_p,
        'each_trade_win_lose_rate': each_trade_win_lose_rate,
        
        # win_lose_pnl_ratio
        'win_lose_pnl_ratio': win_lose_pnl_ratio,
        
        # total natural days duration
        'days':days,
        'anual_return_avg':anual_return_avg
        
    }
    return d

def merged_result_to_csv(dic,path):
    df = pd.DataFrame([dic])
    df.to_csv(path,index=False)
    
def print_merged_result(over_all_summary):
    
    trade_summary_str="""
    win trades:{win_p}({win_rate}), lose trades:{lose_p}({lose_rate}), 
    --------------------------------------------------------------------------
    each_trade_win:{each_trade_win}, each_trade_lose:{each_trade_lose}, each_trade_ratio:{each_trade_ratio}, 
    --------------------------------------------------------------------------

    """.format(
        win_rate="{:.2%}".format(over_all_summary['all_universe_win_rate']),
        lose_rate="{:.2%}".format(over_all_summary['all_universe_lose_rate']),
        win_p="{:.2%}".format(over_all_summary['all_universe_win_pnl_p']),
        lose_p="{:.2%}".format(over_all_summary['all_universe_lose_pnl_p']),
        
        each_trade_win="{:.2%}".format(over_all_summary['average_trade_win_pnl_p']),
        each_trade_lose="{:.2%}".format(over_all_summary['average_trade_lose_pnl_p']),
        each_trade_ratio=over_all_summary['each_trade_win_lose_rate']*-1,
    )
    print(trade_summary_str)
