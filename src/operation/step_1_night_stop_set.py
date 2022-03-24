from datetime import datetime

from operation.lib.migrate_close import back_up_record
from operation.lib.trade_lib import update_record_current_price
import pandas as pd
from version_master.version import op_path_base, op_record


"""
deprecates: this process set stop loss, we run it at night
"""

now = datetime.today()
now_str = now.strftime('%Y-%m-%d')

path_base = op_path_base + now_str
op_path_indicator = path_base + '/indicator/'
# new_record = update_record_current_price(op_path_indicator)


def peak_finder(ticker, indicator_path, start_time):
    start_time_obj = datetime.strptime(start_time, '%m/%d/%Y')

    price_path = indicator_path + ticker + '_downloaded_raw.csv'
    try:
        ticker_df = pd.read_csv(price_path)
    except:
        return {}
    peak = 0
    dt_peak = ''
    for i in range(0, len(ticker_df)):
        high = ticker_df.loc[i, 'high']
        dt = ticker_df.loc[i, 'date']
        dt_obj = datetime.strptime(dt, '%Y-%m-%d')

        if dt_obj<start_time_obj:
            continue
        if high > peak:
            peak = high
            dt_peak = dt
    return {
        'peak':peak,
        'dt_peak':dt_peak
    }

def update_record_stop_price(indicator_path, take_profit_threshold):

    record_path = op_record
    record_df = pd.read_csv(record_path)
    record_df['a_best_price'] = 0
    record_df['a_best_rate'] = 0
    record_df['a_best_price_dt'] = ''
    record_df['a_stop_price'] = 0
    record_df['a_should_have_stop'] = ''
    # a_new_stop_gap
    
    for i in range(0, len(record_df)):
        ticker = record_df.loc[i, 'ticker']
        
        start_time = record_df.loc[i, 'date']
        peak_info = peak_finder(ticker, indicator_path, start_time)
        if len(peak_info) == 0:
            print(ticker,'no price data')
            continue

        # write best price and related info
        record_df.loc[i, 'a_best_price']="{:.2f}".format(round(peak_info['peak'], 2))
        best_rate = (peak_info['peak'] - record_df.loc[i, 'enter_price'])/record_df.loc[i, 'enter_price']
        rate_str = "{:.2f}%".format(round(best_rate*100, 2))
        record_df.loc[i, 'a_best_rate']=rate_str
        record_df.loc[i, 'a_best_price_dt']=peak_info['dt_peak']
        
        
        if best_rate > take_profit_threshold:
            record_df.loc[i, 'a_should_have_stop'] = 'YES'
            x = (peak_info['peak']-record_df.loc[i, 'enter_price'])/2+record_df.loc[i, 'enter_price']
            record_df.loc[i, 'a_stop_price']="{:.2f}".format(round(x, 2))
#             print('limit:', record_df.loc[i, 'limit_order'])
            if record_df.loc[i, 'limit_order'] != '':
                gap_rate_percent = float(record_df.loc[i, 'a_stop_price']) / float(record_df.loc[i, 'limit_order']) - 1
                record_df.loc[i, 'a_new_stop_gap'] = rate_str = "{:.2f}%".format(round(gap_rate_percent*100, 2))
        
            
    record_df.to_csv(record_path, index=False)
    print('best price record updated')

update_record_current_price(op_path_indicator)
update_record_stop_price(op_path_indicator,0.04)
