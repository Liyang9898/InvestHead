from version_master.version import (
    t_20210321_myswing,
    indicator_20210404,
    feature_engineering,
    feature_engineering_split
)
import pandas as pd
import random

df = pd.read_csv(feature_engineering+'features.csv')


def k_split(df,k,to_csv=False):
    batch_size = int(len(df) / k)
    total_len = len(df)
    
    idxs = {}
    for batch_id in range(0,k):
        idxs[batch_id] = []
    
    # assign idx randomly
    for idx in range(0,len(df)):
        batch_id = random.randint(0,k-1)
        idxs[batch_id].append(idx)

    # create sub data frame
    dfs = {}
    for batch_id in range(0,k):
        sub = df.iloc[idxs[batch_id], :]
        assert len(sub) == len(idxs[batch_id])
        assert len(sub) < len(df)
        assert len(df) == total_len
#         print(batch_id, len(sub), total_len)
        if to_csv:
            path = feature_engineering_split+'features_' + str(batch_id) + '.csv'
            sub.to_csv(path, index=False)
        dfs[batch_id] = sub
    
    return dfs

# res = k_split(df,10)
# print(res)