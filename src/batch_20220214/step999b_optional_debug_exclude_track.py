from batch_20201214.reuse_position.reuse_position_lib import merge_n_track_into_one_timeseries
from batch_20220214.batch_20220214_lib.constant import START_DATE, END_DATE, \
    PORTFOLIO_TIME_SERIES_FOLDER_SNP500
import pandas as pd
import plotly.express as px


def aggregate_to_dic(df):
    df['fix'] = df['fix_position']
    df['roll'] = df['roll_position']
    df.reset_index(drop=True, inplace=True)
    gp = df.groupby('date')[['roll','fix']].mean()
    df = gp.reset_index()
    return df


def exclude_track(df, exclude):
    res = df[~df.track_id.isin(exclude)].copy()
    return res


exclude = [40]
output_folder = PORTFOLIO_TIME_SERIES_FOLDER_SNP500
per_track_position_path = f'{output_folder}intermediate_per_track_position.csv'


df = pd.read_csv(per_track_position_path)
df = exclude_track(df, exclude)
uniqueId = df["track_id"].unique() 
print(uniqueId)

gp = aggregate_to_dic(df)

fig = px.line(gp, x="date", y="roll")
fig.show()
