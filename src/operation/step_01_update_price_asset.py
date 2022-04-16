from operation.lib.price_asset_lib import refresh_price_asset
from version_master.version import swing_set1, swing_set_20220103, swing_set_2019_2022

"""
this process download most recent stock price data
"""

refresh_price_asset(time_window=100, set_list=swing_set_2019_2022)

