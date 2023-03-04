'''
Created on Jun 4, 2020

@author: leon
'''
from api.api import api_gen_indicator, api_plot_indicator_from_csv
from global_constant.constant import (
    folder_path_raw_downloaded,
    folder_path_raw_price_formated,
    folder_path_price_with_indicator,
    file_type_postfix
)
from indicator_master.create_indicator_api_main import price_csv_append_indicator


# input file must follow interface: see global_constant file
# output structure: see global_constant file
############################################source region start#############################################
# file_name = "ZM_1D_fmt"
# file_name = "SPY_1D_fmt"
# file_name ="GHSI_1D_fmt"
# file_name = "SPY_1W_fmt"
# file_name = "IWF_1W_fmt"
# file_name = "BTC_1W_fmt"

# file_name = "BTC_1D_fmt"
# file_name = "ETH_1D_fmt"
# file_name = "BNB_1D_fmt"

file_name = "BTC_4H_fmt"
# file_name = "BTC_2H_fmt"
# file_name = "BTC_4H_0718_fmt"
# file_name = "XLK_1W_fmt"
# file_name = "XLK_1D_fmt"

# file_name = "SQ_1D_fmt"
# file_name = "JD_1D_fmt"
# file_name = "BABA_1D_fmt"

# file_name = "ACAD_1D_fmt"
# file_name = "AAN_1D_fmt"
# file_name = "TSLA_1D_fmt" 
# file_name = "WMT_1D_fmt" 
# file_name = "V_1D_fmt"  
# file_name = "FTNT_1D_fmt"
# file_name = "IWF_1D_fmt"
# file_name = "AMD_1D_fmt"  
# file_name = "GOLD_1D_fmt"
# file_name = "EURUSD_1D_fmt"
# file_name = "V_1D_fmt"
# file_name = "SPX_1W_fmt"  
# file_name = "FX_USDCAD_1D_fmt"
############################################source region end#############################################

# this is totally using non-batch folder
indicator_file_postfix = "_idc"
input_file=folder_path_raw_price_formated+file_name+"."+file_type_postfix
output_file=folder_path_price_with_indicator+file_name+indicator_file_postfix+"."+file_type_postfix
print('input:',input_file)
print('writing to',output_file)

# input_file='D:/f_data/price_asset/2021-09-17/format/SPY_downloaded_raw.csv'

api_gen_indicator(
    input_file, 
    output_file,
    "1970-04-01", 
    "2023-04-26",
)
print('output finished: ' + output_file + '  done')
api_plot_indicator_from_csv(output_file)
# print('output finished: ' + output_file + '  done')