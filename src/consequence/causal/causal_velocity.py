def gen_event_p_delta_1d_pct_drop(df, velocity_delta_pct_col, threshold):
    df_selected = df[df[velocity_delta_pct_col] < threshold]
    date_list = df_selected['date'].to_list()
    res = []
    for d in date_list:
        res.append({'date': d})
    return res