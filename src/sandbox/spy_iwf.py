import pandas as pd

path_spy = 'D:/f_data/operation_test/2021-10-12/indicator/SPY_downloaded_raw.csv'
path_iwf = 'D:/f_data/operation_test/2021-10-12/indicator/iwf_downloaded_raw.csv'

df_spy = pd.read_csv(path_spy)
df_iwf = pd.read_csv(path_iwf)
# print(df_spy.columns)

df_spy.rename(columns={'close':'baseline'}, inplace=True)
df_iwf.rename(columns={'close':'experiment'}, inplace=True)

df_spy=df_spy[['date','baseline']].copy()
df_iwf=df_iwf[['date','experiment']].copy()

df = pd.merge(df_spy, df_iwf, on='date')

path_spy_iwf = 'D:/f_data/operation_test/2021-10-12/indicator/spy_iwf.csv'
df.to_csv(path_spy_iwf, index=False)
# print(df)

# df = pd.merge(df_spy, )