from util.util_finance import get_sharpe_ratio_from_list

prices = [30.4, 32.5, 31.7, 31.2, 32.7, 34.1, 35.8, 37.8, 36.3, 36.3, 35.6]
x = get_sharpe_ratio_from_list(prices)
print(x)