
from external_data.index_constituents.change_set_to_time_snapshot import constituents_change_to_time_snapshot
from external_data.index_constituents.index_constituents_lib import  date_format_convert_russell2000, date_format_convert_russell3000, ticket_format
import pandas as pd


# load data 2000
path_2000 = 'D:/f_data/external_data_source/russell2000_component_csv.csv'
path_out_2000 =  'D:/f_data/external_data_source/russell2000_in_different_time.csv'
df_2000 = pd.read_csv(path_2000)
print(df_2000.columns)

# clean 3000
df_2000['date']=df_2000.apply(lambda row : date_format_convert_russell3000(row['date']), axis = 1)
df_2000['ticker_add']=df_2000.apply(lambda row : ticket_format(row['ticker_add']), axis = 1)
df_2000['ticker_del']=df_2000.apply(lambda row : ticket_format(row['ticker_del']), axis = 1)

# convert 3000
df_snapshot_3000 = constituents_change_to_time_snapshot(df_2000)
df_snapshot_3000.to_csv(path_out_2000)

###########################################################################################################

# load data 3000
path_3000 = 'D:/f_data/external_data_source/russell3000_component_csv.csv'
path_out_3000 =  'D:/f_data/external_data_source/russell3000_in_different_time.csv'
df_3000 = pd.read_csv(path_3000)
print(df_3000.columns)

# clean 3000
df_3000['date']=df_3000.apply(lambda row : date_format_convert_russell3000(row['date']), axis = 1)
df_3000['ticker_add']=df_3000.apply(lambda row : ticket_format(row['ticker_add']), axis = 1)
df_3000['ticker_del']=df_3000.apply(lambda row : ticket_format(row['ticker_del']), axis = 1)

# convert 3000
df_snapshot_3000 = constituents_change_to_time_snapshot(df_3000)
df_snapshot_3000.to_csv(path_out_3000)