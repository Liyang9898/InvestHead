from external_data.index_constituents.index_constituents_lib import ticket_format
import pandas as pd

ADD='add'
DEL='del'

def constituents_change_to_time_snapshot(df):

    # extract time 
    month_list = df['date'].unique()
    month_list.sort()
    sorted_month_list = list(month_list)
    print(sorted_month_list)
    
    # change set
    change_set = {} # map<time, map<add/del, map<ticker,company_name>>>
    for t in sorted_month_list:
        change_set[t] = {ADD:{}, DEL:{}}
        
    for i in range(0, len(df)):
        date = df.loc[i, 'date']
        
        ticker_add = df.loc[i, 'ticker_add']
        company_name_add = df.loc[i, 'company_name_add']
        
        ticker_del = df.loc[i, 'ticker_del']
        company_name_del = df.loc[i, 'company_name_del']
        
        if ticker_add != '':
            change_set[date][ADD][ticker_add] = company_name_add
        if ticker_del != '':    
            change_set[date][DEL][ticker_del] = company_name_del
        
    # for t, v in change_set.items():
    #     print(t, len(v[ADD]), len(v[DEL]))
    

    collection = {} # MAP<date, MAP<ticker, company name>>
    moving_collection = {} # MAP<ticker, company name>
    rows = []
    
    for t in sorted_month_list:
        add_set = change_set[t][ADD]
        del_set = change_set[t][DEL]
        for ticker, company_name in add_set.items():
            moving_collection[ticker] = company_name
        for ticker, company_name in del_set.items():
            if ticker not in moving_collection:
                continue
            del moving_collection[ticker]
        collection[t] = moving_collection
        ticker_set = list(moving_collection.keys())
        row = {'time': t, 'cnt': len(moving_collection), 'stock': '|'.join(ticker_set)}
        print(t, len(moving_collection))
        rows.append(row)
        
    df = pd.DataFrame(rows)
    return df

