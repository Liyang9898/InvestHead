import plotly.graph_objects as go



def draw_chat(x3, x7, x14,t3,t7,t14,title):
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=x3,
        histnorm='percent',
        name=t3, # name used in legend and hover labels
        marker_color='#EB89B5',
        opacity=0.75
    ))
    fig.add_trace(go.Histogram(
        x=x7,
        histnorm='percent',
        name=t7,
        marker_color='#330C73',
        opacity=0.75
    ))
    fig.add_trace(go.Histogram(
        x=x14,
        histnorm='percent',
        name=t14,
        marker_color='#555573',
        opacity=0.75
    ))
    
    fig.update_layout(
        title_text=title, # title of plot
#         xaxis_title_text='Value', # xaxis label
#         yaxis_title_text='Count', # yaxis label
#         bargap=0.2, # gap between bars of adjacent location coordinates
#         bargroupgap=0.1 # gap between bars of the same location coordinates
    )
    
    fig.show()
    
    
def draw_chat_6(x1,x2,x3,x4,x5,x6,t1,t2,t3,t4,t5,t6,title):
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=x1,
        histnorm='percent',
        name=t1, # name used in legend and hover labels
        marker_color='#EB89B5',
        opacity=0.75
    ))
    fig.add_trace(go.Histogram(
        x=x2,
        histnorm='percent',
        name=t2,
        marker_color='#330C73',
        opacity=0.75
    ))
    fig.add_trace(go.Histogram(
        x=x3,
        histnorm='percent',
        name=t3,
        marker_color='#555573',
        opacity=0.75
    ))
    
    fig.add_trace(go.Histogram(
        x=x4,
        histnorm='percent',
        name=t4, # name used in legend and hover labels
        marker_color='#EB43B5',
        opacity=0.75
    ))
    fig.add_trace(go.Histogram(
        x=x5,
        histnorm='percent',
        name=t5,
        marker_color='#220C73',
        opacity=0.75
    ))
    fig.add_trace(go.Histogram(
        x=x6,
        histnorm='percent',
        name=t6,
        marker_color='#115573',
        opacity=0.75
    ))
    
    fig.update_layout(
        title_text=title, # title of plot
#         xaxis_title_text='Value', # xaxis label
#         yaxis_title_text='Count', # yaxis label
#         bargap=0.2, # gap between bars of adjacent location coordinates
#         bargroupgap=0.1 # gap between bars of the same location coordinates
    )
    
    fig.show()