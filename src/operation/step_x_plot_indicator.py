
import pandas as pd
from indicator_master.plot_indicator_lib import plot_indicator

from version_master.version import op_path_base
from datetime import datetime, timedelta

ticker = 'BTC-USD'

def plot_chart(ticker):
    # path builder
    now = datetime.today()
    now_str = now.strftime('%Y-%m-%d')
    path_base = op_path_base + now_str
    op_path_indicator = path_base + '/indicator/'
    path = op_path_indicator + ticker + '_downloaded_raw.csv'
    
    # plot
    df= pd.read_csv(path)
    plot_indicator(df, 'sequence_8_21_50',ticker)
    
    
plot_chart(ticker)