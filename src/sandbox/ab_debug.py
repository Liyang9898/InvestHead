import pandas as pd
from util.util_finance import compute_alpha_beta_from_position


path = 'D:/f_data/perf_compare/fb_vs_spy_2021-10-17_18-02-27_3446/asset/merge.csv'
df = pd.read_csv(path)
# print(df)
date_col='date'
period = 'month'


base_col='baseline'
exp_col = 'experiment'

# base_col='experiment'
# exp_col = 'baseline'



x = compute_alpha_beta_from_position(df, date_col, base_col, exp_col, period)
print(x)