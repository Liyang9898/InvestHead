'''
Created on Feb 24, 2023

@author: spark
'''
from api.api import api_plot_indicator_from_csv


dic = ['XLC', 'XLY', 'XLP', 'XLE', 'XLF', 'XLV', 'XLI', 'XLK', 'XLB', 'XLRE', 'XLU']
ticker = 'XLK'

for ticker in dic:
    sector_idc_path = "C:/f_data/sector/indicator/{ticker}_1W_fmt_idc.csv".format(ticker=ticker)
    api_plot_indicator_from_csv(sector_idc_path)