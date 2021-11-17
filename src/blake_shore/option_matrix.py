from blake_shore.data.options import (
    fb_options_3m,
    amzn_options_3m,
    amd_options_3m,
    tsla_options_2m,
    ttc_options_2m,
    pool_options_3m,
    morn_options_4m,
    fb_options_5m,
    tsla_options_4m,
    tsla_options_7m,
    ttc_options_6m,
    rol_options_3m,
    vrsn_options_2m,
    bro_options_4m,
    tru_options_4m,
    shw_options_4m,
    xpo_options_3m,
    apo_options_4m,
    it_options_4m,
)
from blake_shore.lib.generate_trail import batch_gen_option_trail_from_today_option
from blake_shore.lib.helper import iv_and_leverage_from_option_group, option_jacker_negation_price
import pandas as pd


option_bundle = [
    fb_options_3m,
    amzn_options_3m,
    amd_options_3m,
    tsla_options_2m,
    ttc_options_2m,
    pool_options_3m,
    morn_options_4m,
    fb_options_5m,
    tsla_options_4m,
    tsla_options_7m,
    ttc_options_6m
]


option_bundle_random_day = [
    rol_options_3m,
    vrsn_options_2m,
    bro_options_4m,
    tru_options_4m,
    shw_options_4m,
    xpo_options_3m,
    apo_options_4m,
    it_options_4m,
    
]


def get_option_bundle_iv_leverage_matric(option_bundle, reverse_stock_growth=False):
    rows = []
    for options in option_bundle:
        # for negative jack
        if reverse_stock_growth:
            options = option_jacker_negation_price(options)
    
        print(f"process{options}")
    
        dfs = batch_gen_option_trail_from_today_option(options)
        meta = iv_and_leverage_from_option_group(dfs)
        rows.append(meta)
        
    df = pd.DataFrame(rows)
    df = df[['ticker','expire_month','iv_0','leverage_0','iv_avg','leverage_avg']]
    df.sort_values(by=['iv_0'], inplace=True)
    return df

# matrix = get_option_bundle_iv_leverage_matric(option_bundle)
# print(matrix)

matrix_neg = get_option_bundle_iv_leverage_matric(option_bundle, reverse_stock_growth=True)
matrix_neg.to_csv('D:/f_data/matrix_pos.csv', index=False)
print(matrix_neg)
# fig_avg = px.scatter(matrix, x="iv_avg", y="leverage_avg", title='iv-leverage relationship')
# fig_avg.show()
# fig_0 = px.scatter(matrix, x="iv_0", y="leverage_0", title='iv-leverage relationship')
# fig_0.show()