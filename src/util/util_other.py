from util.util import merge_dict_by_key
import pandas as pd

def to_df_custome_1(cash_position):
    merged_dict = merge_dict_by_key(cash_position['price_position'], cash_position['cash_rollover_position'], 'baseline', 'test')
    rows = []
    for k, v in merged_dict.items():
        k = str(k)
        k = k.split(" ")[0]
        v['date'] = k
        rows.append(v)
    df = pd.DataFrame(rows)
    return df
    