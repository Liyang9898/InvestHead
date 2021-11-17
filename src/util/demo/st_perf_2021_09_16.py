import pandas as pd
from util.util_finance import single_protfolio_perf


path = 'D:/f_data/temp/movingwindow_test.csv'
df = pd.read_csv(path)

for sb in df.columns:
    if sb == 'date':
        continue
    perf = single_protfolio_perf(df=df, date_col='date', position_col=sb, symbol=sb)
    print(perf)