from price_asset_master.lib.api.api_download_ticker_lib import download_format_2csv

def download_ticker(ticker, start, end, path_out, interval):
    """
    interval : str
            Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    """
    download_format_2csv(ticker, start, end, path_out, interval)