import pandas as pd
from version_master.version import (
    op_record,
)


def get_portafolio_summary():
    df = pd.read_csv(op_record)
    st_cnt = len(df)
    df['st_value'] = df['quantity'] * df['current_price']
    total_val = df['st_value'].sum()
    str = f"total value: {total_val}, stock cnt: {st_cnt}"
    return str
