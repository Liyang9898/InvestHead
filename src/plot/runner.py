
def run(trades, contract_price, start):
    total_balance = {}
    daily_pnl_dic = {}
    daily_contract = {}
    cur = start
    for ds, trade in trades.items():
        if cur < contract_price:
            break
        contract_cnt = min(cur, start) / contract_price
        daily_pnl = trade['pnl'] * 10 * 50 * contract_cnt
        cur = cur + daily_pnl
        total_balance[ds] = cur
        daily_contract[ds] = contract_cnt
        daily_pnl_dic[ds] = daily_pnl
    return {
        'balance':total_balance,
        'contract':daily_contract,
        'daily_pnl':daily_pnl_dic
    }