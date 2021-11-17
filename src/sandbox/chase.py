import pandas as pd


path = 'D:/f_data/temp/Chase6669_Activity20210327_20210426_20210428.csv'

df=pd.read_csv(path)
df=df[df['Type']=='Sale']

des_gp = df.groupby(['Description'])['Amount'].sum()
print(des_gp)

cate_gp = df.groupby(['Category'])['Amount'].sum()
print(cate_gp)