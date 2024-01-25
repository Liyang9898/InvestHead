'''
Created on Jun 8, 2020

@author: leon
'''
from indicator_master.raw_stock_reader_lib import load_df_from_csv 
from indicator_master.indicator_compute_lib import add_indicator
from indicator_master.plot_indicator_lib import plot_indicator
from indicator_master import constant
from global_constant import constant as constant2
import pandas as pd

folder_path_raw_downloaded = constant2.folder_path_raw_downloaded
folder_path_raw_price_formated = constant2.folder_path_raw_price_formated
folder_path_price_with_indicator = constant2.folder_path_price_with_indicator
file_type_postfix=constant2.file_type_postfix

def pickcolumn(file, path_out, input_column):
    path = file
    df = pd.read_csv(path)

    # df.rename(columns={
    #     "MA": "ma200", 
    #     "MA.1": "ma50",
    #     "EMA": "ema21",
    #     "EMA.1": "ema8",
    # }, inplace=True)

    print('df reading done')
    df.to_csv(
        path_out,
        columns=constant.price_interface,
        index=False
    )
    print('csv output done')

############################################source region start#############################################
raw_price_file_name = "BATS_SPY, 1D"
path_out_file_name = """SPY_1D_fmt"""  

# raw_price_file_name = "BATS_ZM, 1D"
# path_out_file_name = """ZM_1D_fmt"""  

# raw_price_file_name = "BATS_SPY, 1W"
# path_out_file_name = """SPY_1W_fmt"""  
# 
# raw_price_file_name = "BATS_GHSI, 1D"
# path_out_file_name = """GHSI_1D_fmt"""  

# raw_price_file_name ="BITSTAMP_BTCUSD, 1W" 
# path_out_file_name = "BTC_1W_fmt"  

# raw_price_file_name ="BITSTAMP_BTCUSD, 1D" 
# path_out_file_name = "BTC_1D_fmt"  

# raw_price_file_name ="BINANCE_ETHUSD, 1D" 
# path_out_file_name = "ETH_1D_fmt"  

# raw_price_file_name ="BINANCE_BNBUSD, 1D" 
# path_out_file_name = "BNB_1D_fmt"  

# raw_price_file_name ="BITSTAMP_BTCUSD, 4H" 
# path_out_file_name = "BTC_4H_fmt"  

# raw_price_file_name ="BITSTAMP_BTCUSD, 2H" 
# path_out_file_name = "BTC_2H_fmt"  

# raw_price_file_name ="BATS_XLK, 1W" 
# path_out_file_name = "XLK_1W_fmt"  

# raw_price_file_name ="BATS_XLK, 1D" 
# path_out_file_name = "XLK_1D_fmt"  

# raw_price_file_name ="BATS_BABA, 1D" 
# path_out_file_name = "BABA_1D_fmt"  
 
# raw_price_file_name ="BATS_JD, 1D" 
# path_out_file_name = "JD_1D_fmt"  
 
# raw_price_file_name ="BATS_SQ, 1D" 
# path_out_file_name = "SQ_1D_fmt"  

# raw_price_file_name ="BATS_ACAD, 1D" 
# path_out_file_name = "ACAD_1D_fmt"  

# raw_price_file_name ="BATS_TSLA, 1D" 
# path_out_file_name = "TSLA_1D_fmt"  

# raw_price_file_name ="BATS_WMT, 1D" 
# path_out_file_name = "WMT_1D_fmt"  

# raw_price_file_name ="BATS_V, 1D" 
# path_out_file_name = "V_1D_fmt"  
# 
# # BATS_IWF, 1D
# raw_price_file_name ="BATS_IWF, 1D" 
# path_out_file_name = "IWF_1D_fmt"  

# raw_price_file_name ="BATS_IWF, 1W" 
# path_out_file_name = "IWF_1W_fmt"  

# raw_price_file_name ="BATS_AMD" 
# path_out_file_name = "AMD_1D_fmt"  

# raw_price_file_name = "OANDA_EURUSD, 1D" 
# path_out_file_name = "EURUSD_1D_fmt"  

# raw_price_file_name = "BATS_V, 1D"
# path_out_file_name = "V_1D_fmt"  
#
# raw_price_file_name = "SP_SPX, 1W_allhist"
# path_out_file_name = "SPX_1W_fmt"  

# raw_price_file_name ="FX_USDCAD, 1D" 
# path_out_file_name = "FX_USDCAD_1D_fmt" 
############################################source region end#############################################

raw_price_files=folder_path_raw_downloaded+raw_price_file_name+"."+file_type_postfix
path_out=folder_path_raw_price_formated+path_out_file_name+"."+file_type_postfix

input_column=['time', 'open','high','low','close','Volume','volume_ma','ma200','ma50','ema21','ema8']

pickcolumn(raw_price_files, path_out, input_column)

print(raw_price_files)
print(path_out)