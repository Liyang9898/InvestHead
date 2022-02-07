from batch_20211116.batch_20211116_lib.constant import TICKER_RANK_FOLDER
from util.util_file import get_all_csv_file_in_folder
import pandas as pd

 
def gen_stock_rank_artifact(rank_csv_folder):
    """
    input: csv folder path
    output: map<year, df>
    """
      
    # get list of ticker ranking files
    files = get_all_csv_file_in_folder(rank_csv_folder)
    df_map = {}
    for file in files:
        # deal with key
        tokens = file.split('/')
        file_key = tokens[-1].replace('.csv', '')
        """
        file_name: start_date, end_date (of the history length)
        so the meaningful use case for this history is end_date and onward
        key = year of end_date
        meaning, if today is in year {year}, that's the ranking record you should use
        """
        end_date = file_key.split('_')[1]
        year = end_date.split('-')[0]

        # read data
        df = pd.read_csv(file)
        df_map[year] = df

        
    return df_map
          
