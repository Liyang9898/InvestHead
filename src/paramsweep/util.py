import datetime

def gen_date_rage_list(start,end,range_days):
    res = []
    
    start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end, "%Y-%m-%d")
    cur_start = start_date
    cur_end = cur_start + datetime.timedelta(days=range_days)
    while cur_end < end_date:
        pair = {
            's':cur_start.strftime("%Y-%m-%d"),
            'e':cur_end.strftime("%Y-%m-%d")
        }
        res.append(pair)
        cur_start = cur_end
        cur_end = cur_start + datetime.timedelta(days=range_days)
    return res