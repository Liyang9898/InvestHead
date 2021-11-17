
import pandas as pd
from util.util_finance import get_beta_from_list
from version_master.version import t_20210425_ema21_ma50_gap_per_ticker_4p_out


# path = t_20210425_ema21_ma50_gap_per_ticker_4p_out + """merge/ui_backend_data.csv"""
path = 'C:/Users/leon/Desktop/beta_test.csv'
df = pd.read_csv(path)
print(df.columns)

x = df['spy_normalized'].tolist()
y = df['portfolio_normalized'].tolist()

print(x)
print(y)

beta = get_beta_from_list(x,y)
print(beta)
