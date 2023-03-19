'''
Created on Mar 19, 2023

@author: spark
'''
from numpy import NaN
# import plotly.express as px
import pandas as pd
from util.util_pandas import df_normalize, dict_to_df
from util.util_time import df_filter_dy_date, days_gap_date_str, count_weekday


def prepare_ticker_df_dict(allo_df):
    ticker_df_dict = {}
    for ticker in allo_df.columns:
        if 'date' in ticker:
            continue    
        ticker_path = "C:/f_data/sector/indicator_day/{ticker}_1D_fmt_idc.csv".format(ticker=ticker)
        ticker_df = pd.read_csv(ticker_path)
        
        # reformat
        ticker_df['ts'] = ticker_df['close']
        ticker_df = ticker_df[['date', 'ts']]
        ticker_df = ticker_df.copy()
        ticker_df_dict[ticker] = ticker_df
    return ticker_df_dict
        
        
def build_aum(allo_df, ticker_df_dict):
    '''
    assuming always taking action in the morning, track perf in the afternoon
    for allo, this dic means between the open of start date and open of the end date, the allocation is like the df
    '''
    pre_aum_end = 1
    aum_all_df_list = []
    aum_ticker_df_list = []
    
    for i in range(0, len(allo_df)):
        start_date = allo_df.loc[i, 'start_date']
        end_date = allo_df.loc[i, 'end_date']
        print(start_date + ' ' + end_date)
        period_gap = days_gap_date_str(start_date, end_date)
        if period_gap == 0:
            continue
        
        # validate: time period must be one day
        assert period_gap > 0
        
        '''
        Step 1: get start AUM of each ticket -> ticker_start_aum_dic <ticker, AUM of this ticker>
        total aum start at 1
        '''
        allo_dic = {}
        allo_sum = 0
        for ticker in allo_df.columns:
            if 'date' in ticker:
                continue
            if allo_df.loc[i, ticker] is not NaN and allo_df.loc[i, ticker] > 0:
                allo_dic[ticker] = allo_df.loc[i, ticker]
                allo_sum = allo_sum + allo_df.loc[i, ticker]
        assert allo_sum - 1 < 0.001
        
        ticker_start_aum_dic = {}
        ticker_start_aum_sum = 0
        for ticker, v in allo_dic.items():
            ticker_start_aum_dic[ticker] = v * pre_aum_end
            ticker_start_aum_sum += ticker_start_aum_dic[ticker]
        
        ######## valicate:start AUM sume up right, has at least one ticker
        assert abs(ticker_start_aum_sum / pre_aum_end - 1) < 0.001
        assert len(ticker_start_aum_dic) > 0
        ######## validation
        
        print('ticker AUM start' + str(ticker_start_aum_dic))
        
        '''
        Step 2: get ts per ticker and filter 
        '''
        ticker_ts_df_filtered_scaled = {}
        first_trade_date = ''
        for ticker in ticker_start_aum_dic.keys():
            init_aum = ticker_start_aum_dic[ticker]
            ticker_df = ticker_df_dict[ticker].copy()
            ticker_df_filter = df_filter_dy_date(ticker_df, 'date', start_date, end_date)
            '''
            Step 3: scale the time series in previous step -> ticker_ts_df_filtered_scaled <ticker, df in that time range, scaled> cols: date, ts
            '''
            ticker_df_filter_norm = df_normalize(ticker_df_filter, 'ts', init_aum)
            ticker_df_filter_norm.reset_index(inplace=True, drop=True)
            
            ######## validation: 
            # real time gap is less than 4 days from time period in csv
            # number of days with data is correct
            # initial aum match step 1
            # start end ratio same after scale
            
            assert init_aum == ticker_df_filter_norm.loc[0, 'ts']
            assert len(ticker_df_filter_norm) > 0    
            norm_change = ticker_df_filter_norm.loc[len(ticker_df_filter_norm) - 1, 'ts'] / ticker_df_filter_norm.loc[0, 'ts'] - 1
            ori_change = ticker_df_filter.loc[len(ticker_df_filter) - 1, 'ts'] / ticker_df_filter.loc[0, 'ts'] - 1
            assert abs(norm_change-ori_change) < 0.001
            start_date_real = ticker_df_filter_norm.loc[0, 'date']
            
            # all ticker start on the same trade date
            if first_trade_date == '':
                first_trade_date = start_date_real
            else:
                assert first_trade_date == start_date_real
            
            end_date_real = ticker_df_filter_norm.loc[len(ticker_df_filter_norm) - 1, 'date']
            period_gap = days_gap_date_str(start_date, end_date)
            perid_gap_real = days_gap_date_str(start_date_real, end_date_real)

            assert perid_gap_real > 0
            assert period_gap >= perid_gap_real
            
            assert period_gap - perid_gap_real < 5
            work_day = count_weekday(start_date, end_date)
            trading_day = len(ticker_df_filter_norm)
            trading_day_work_day_ratio =  trading_day  * 1.0 / work_day

            assert trading_day_work_day_ratio > 5/7

            # assert trading_work_day_ratio
            ######## validation
            
            ticker_ts_df_filtered_scaled[ticker] = ticker_df_filter_norm
            
            
            ticker_df_filter_norm_add_col = ticker_df_filter_norm.copy()
            ticker_df_filter_norm_add_col['ticker'] = ticker
            aum_ticker_df_list.append(ticker_df_filter_norm_add_col)
        
        ######## validate: same count, total sum same
        assert len(ticker_ts_df_filtered_scaled) == len(ticker_start_aum_dic)
        ######## validation
        
        
        '''
        Step 4: aggregate all ticker AUM -> aum_all_df (a df of time series of AUM) cols: date,ts
        '''
        
        
        aum_dic = {}
        for ticker, ticker_aum_df in ticker_ts_df_filtered_scaled.items():
            for i in range(0, len(ticker_aum_df)):
                date = ticker_aum_df.loc[i, 'date']
                ts = ticker_aum_df.loc[i, 'ts']
                if date not in aum_dic:
                    aum_dic[date] = 0
                aum_dic[date] = aum_dic[date] + ts
                
        aum_all_df = dict_to_df(aum_dic, 'date', 'ts')
        
        # validation
        assert first_trade_date == aum_all_df.loc[0, 'date']
        
        aum_start = aum_all_df.loc[0, 'ts']
        aum_end = aum_all_df.loc[len(aum_all_df) - 1, 'ts']
        
        sum_start = 0
        sum_end = 0
        for ticker, ticker_df in ticker_ts_df_filtered_scaled.items():
            sum_start = sum_start + ticker_df.loc[0, 'ts']
            sum_end = sum_end + ticker_df.loc[len(ticker_df) - 1, 'ts']
            
            assert len(aum_all_df) <= len(ticker_df) + 4
        

        assert abs(sum_start / aum_start - 1) < 0.001
        assert abs(sum_end / aum_end - 1) < 0.001
        assert abs(aum_start / pre_aum_end - 1) < 0.001

        print('Period AUM Start End: ' + str(aum_start) + ' ' + str(aum_end))
        aum_all_df_list.append(aum_all_df)
        pre_aum_end = aum_end
        
        
    '''
    Step 5: concat
    '''
    aum_all_df_merged = pd.concat(aum_all_df_list, axis=0, ignore_index=True)
    aum_ticker_df_merged = pd.concat(aum_ticker_df_list, axis=0, ignore_index=True)
    
    return {
        'all': aum_all_df_merged,
        'ticker': aum_ticker_df_merged
    }
    
        
# path_allocation = "C:/f_data/sector/allocation/allocation_ema21_below_ma50_recent_pnl_past_1_month_ranked_top3_increase_only.csv"
# allo_df = pd.read_csv(path_allocation)
# print(allo_df)       
#
#
# # get start aum of each ticket
# ticker_df_dict = prepare_ticker_df_dict(allo_df)
#
# aum_ts = build_aum(allo_df, ticker_df_dict)
# aum_all_df_merged = aum_ts['all']
# aum_ticker_df_merged = aum_ts['ticker']
#
# path_aum_all_df_merged = "C:/f_data/sector/debug/aum_all_df_merged_dev.csv"
# path_aum_ticker_df_merged = "C:/f_data/sector/debug/aum_ticker_df_merged_dev.csv"
#
# aum_all_df_merged.to_csv(path_aum_all_df_merged, index=False)
# aum_ticker_df_merged.to_csv(path_aum_ticker_df_merged, index=False)
#
# fig = px.line(aum_all_df_merged, x="date", y="ts", title='sector_remix')
# fig.show()   
#
# fig_sector = px.scatter(aum_ticker_df_merged, x="date", y="ts", color='ticker', title='sector_remix')
# fig_sector.show()   
        