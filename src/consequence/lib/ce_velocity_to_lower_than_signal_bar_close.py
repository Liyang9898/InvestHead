from consequence.causal.causal_velocity import gen_event_p_delta_1d_pct_drop
from consequence.effect.effect_lower_than_close import min_price_future
import pandas as pd
import plotly.express as px
from util.util import PX_PERCENT_HIST, percentile_from_list
import plotly.graph_objects as go

def velocity_to_lower_than_signal_bar_close(df, date_idx_map, signal, threshold, observe_range, plot=False):
    events = gen_event_p_delta_1d_pct_drop(df, signal, threshold)
    effects = []
    for event in events:
        effect = min_price_future(df, date_idx_map, observe_range, event)
        effects.append(effect)
    effect_df = pd.DataFrame(effects)
    effect_df['signal']=signal
    effect_df['threshold']=threshold
    
    effect_df_positive = effect_df[effect_df['label']==True]
    effect_df_negative = effect_df[effect_df['label']==False]
    conclusion = {
        'signal':signal,
        'threshold':threshold,
        'sample size:': len(effect_df), 
        'true_rate':len(effect_df_positive)/len(effect_df)
    }
    print(conclusion)
    
    pnl_drop = effect_df_positive['val'].to_list()
    
    if plot:
        fig = px.histogram(effect_df, x="val", histnorm=PX_PERCENT_HIST, nbins=30)
        fig.show()

        fig2 = go.Figure(data=[go.Histogram(x=pnl_drop, cumulative_enabled=True,xbins=dict(size=0.001),histnorm=PX_PERCENT_HIST)])
        fig2.show()
        
        fig3 = px.histogram(effect_df_positive, x="day", histnorm=PX_PERCENT_HIST)
        fig3.show()
    
    return effect_df
