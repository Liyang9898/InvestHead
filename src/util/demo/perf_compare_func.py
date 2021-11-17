from util.util_portfolio_perf_compare import perf_compare_with_download

start_date = '1991-10-17'
end_date = '2022-10-17'
baseline_ticket = 'spy'
experiment_ticker = 'iwf'

# ivw spy
# iwf iwb(vone)

perf_compare_with_download(baseline_ticket, experiment_ticker, start_date, end_date)