import pandas as pd
import plotly.graph_objects as go
from datetime import date
from plotly.subplots import make_subplots


def draw_plot(df_orig, col, cols_list, second_label, time_range, plot_types):

    # --- 1. x ticks preparation
    if time_range == 1:
        df = df_orig[-30:]
        dt = pd.to_datetime(df['timestamp'], format="%d.%m.%Y %H:%M")
        xticks_val = list(range(len(dt)))[0::round(len(df)/10)]
        xticks_lab = [str(date(x.year, x.month, x.day).strftime("%d.%m"))
                      for x in dt.iloc[xticks_val]]

    elif time_range == 2:
        df = df_orig[-365:]
        dt = pd.to_datetime(df['timestamp'], format="%d.%m.%Y %H:%M")
        xticks_val = list(range(len(dt)))[0::round(len(df)/10)]
        xticks_lab = [str(date(x.year, x.month, x.day).strftime("%m/%y"))
                      for x in dt.iloc[xticks_val]]

    elif time_range == 3:
        df = df_orig[-365*5:]
        dt = pd.to_datetime(df['timestamp'], format="%d.%m.%Y %H:%M")
        xticks_val = list(range(len(dt)))[0::round(len(df)/10)]
        xticks_lab = [str(date(x.year, x.month, x.day).strftime("%m/%y"))
                      for x in dt.iloc[xticks_val]]

    elif time_range == 4:
        df = df_orig
        dt = pd.to_datetime(df['timestamp'], format="%d.%m.%Y %H:%M")
        xticks_val = list(range(len(dt)))[0::round(len(df) / 10)]
        xticks_lab = [str(date(x.year, x.month, x.day).strftime("%Y"))
                      for x in dt.iloc[xticks_val]]

    else:
        df = df_orig
        xticks_val = []
        xticks_lab = []

    # --- 2. Secondary plot preparation
    average_price = df[cols_list].mean(axis=1)

    # --- 3. Make plot
    graph = make_subplots(specs=[[{"secondary_y": True}]])

    if 1 in plot_types:
        graph.add_trace(
            go.Scatter(x=df['timestamp'], y=df[col], marker=dict(color="blue"),
                       name=col.replace('-', ' / ')),
            secondary_y=False)

    if 2 in plot_types:
        graph.add_trace(
            go.Scatter(x=df['timestamp'], y=average_price,
                       marker=dict(color="red"), name=second_label),
            secondary_y=True)

    # --- 4. Style plot
    graph.update_layout(margin=dict(t=25, r=0, l=0, b=35), showlegend=True)
    graph.update_xaxes(tickangle=30, tickfont=dict(size=10),
                       tickvals=xticks_val, ticktext=xticks_lab)
    graph.update_yaxes(title_text="", secondary_y=False, color="blue")
    graph.update_yaxes(title_text="", secondary_y=True, color="red")

    return graph
