from feature_engineering.cross_validation.k_fold_validation import k_fold_validation, \
    cross_validation_auto_cut
import pandas as pd
from version_master.version import (
    feature_engineering,
)


df = pd.read_csv(feature_engineering+'features.csv')
 
# res = k_fold_validation(df,2)
# print(res)
df=df[df['ticker']=='Y']

res_auto = cross_validation_auto_cut(df)
print(res_auto)