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
    ttc_options_6m
)
from blake_shore.lib.generate_trail import batch_gen_option_trail_from_today_option
from blake_shore.lib.helper import iv_and_leverage_from_option_group
from blake_shore.lib.visual import ploty_stock_option_batch, \
    ploty_leverage_batch


dfs = batch_gen_option_trail_from_today_option(fb_options_3m, negative_growth=True)

res = iv_and_leverage_from_option_group(dfs)
print(res)
ploty_stock_option_batch(dfs)
ploty_leverage_batch(dfs, absolute=True)
ploty_leverage_batch(dfs, absolute=False)