
def min_price_future(df, date_idx_map, offset, event):
    start=event['date']
    i = date_idx_map[start]
    price = df.loc[i, 'close']
    
    min_price = 9999999
    min_day = 0
    day_cnt = 1
    min_date = None
    for idx in range(i + 1, min(i + offset + 1, len(df))):
        low = df.loc[idx, 'low']
        if low < min_price:
            min_price = low
            min_day = day_cnt
            min_date = df.loc[idx, 'date']
        day_cnt += 1
    
    price_delta = min_price / price - 1
    label = True if price_delta < 0 else False
    res = {
        'event_date': start,
        'decrease': price_delta,
        'day': min_day,
        'min_date': min_date,
        'label': label,
        'val': price_delta
    }
    return res