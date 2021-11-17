from spy_volocity_study.lib.constant import S, S2, E
import plotly.graph_objects as go


def ploty_velocity_adjust_ui(df, col_names, adjustments):
    # UI    
    fig = go.Figure()
    
    for col in col_names:
        fig.add_trace(go.Scatter(
            x=df['date'], 
            y=df[col],     
            mode='lines+markers',
            name=col
        ))
    
    for adjustment in adjustments:
        fig.add_vrect(
            x0=adjustment[S], 
            x1=adjustment[S2], 
            annotation_text="adj", 
            annotation_position="top left",
            fillcolor="red", 
            opacity=0.25, 
            line_width=0
        )
        fig.add_vrect(
            x0=adjustment[S2], 
            x1=adjustment[E], 
            # annotation_text="drop", 
            annotation_position="top left",
            fillcolor="black", 
            opacity=0.25, 
            line_width=0
        )
    fig.update_yaxes(dtick=0.01)
    fig.show()
    