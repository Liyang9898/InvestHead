
def next_bar_date(df, date_col, feature_col):
    """
    feature_col has next bar's date
    """
    df[feature_col] = df[date_col].shift(-1)