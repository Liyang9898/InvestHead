import pandas as pd
from util.util_finance import multi_protfolio_perf


path = 'D:/f_data/temp/etf_strategy/uni.csv'
df = pd.read_csv(path)

multi_protfolio_perf(
    df=df, 
    date_col='date', 
    baseline_position_col='price', 
    exp_position_cols=['21_50', '8_21_50_exit']
)
    