'''
Created on Mar 3, 2021

@author: leon
'''
from version_master.version import (
    trade_swing_2150in_2150out_20210302_iwf_channel,
    indicator_20210301
)
from batch_20201214.cach_history._multi import idle_position_cash_history

trade_folder=trade_swing_2150in_2150out_20210302_iwf_channel
indicator_folder=indicator_20210301
start_time="2016-01-01 20:00:00"
end_time="2020-12-31 19:00:00"

idle_position_cash_history(
    start_time,
    end_time,
    trade_folder,
    indicator_folder,
)