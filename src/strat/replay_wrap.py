from strat.replay_xx import replay_xx
from strat.replay_xxtill import replay_xxtill

def replay(df_day, end_time, stop_gain, stop_loss, open_top, threshold):
    if open_top:
        return replay_xxtill(df_day, end_time, stop_gain, stop_loss, threshold)
    else:
        return replay_xx(df_day, end_time, stop_gain, stop_loss, threshold)