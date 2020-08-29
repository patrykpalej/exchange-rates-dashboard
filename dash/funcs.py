import pickle
import pandas as pd
from datetime import date, datetime
import plotly.graph_objects as go
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


def draw_big_plot(days_range, values, values_dict, checklist):
    # 1. Preparation
    if len(days_range) < 365:
        xticks_idx \
            = list(range(len(days_range)))[0::round(len(values) /
                                                    min(len(days_range), 10))]
        xticks_lab = [str(date(x.year, x.month, x.day).strftime("%d.%m"))
                      for x in [days_range[y] for y in xticks_idx]]
        xticks_val = [days_range[x] for x in xticks_idx]
        xlabel \
            = str(days_range[0].year) \
            if days_range[0].year == days_range[-1].year \
            else str(days_range[0].year) + "/" + str(days_range[-1].year)
    else:
        xticks_idx = list(range(len(days_range)))[0::round(len(values)/10)]
        xticks_lab = [str(date(x.year, x.month, x.day).strftime("%m/%y"))
                      for x in [days_range[y] for y in xticks_idx]]
        xticks_val = [days_range[x] for x in xticks_idx]
        xlabel = ""

    # 2. Plot drawing
    color_dict = {"USD": "green", "EUR": "blue", "GBP": "orange", "CHF": "red"}

    graph = make_subplots()

    graph.update_xaxes(title_text=xlabel, tickvals=xticks_val,
                       ticktext=xticks_lab)
    graph.update_yaxes(title_text="Wartość portfela [PLN]",
                       titlefont=dict(size=18))
    graph.update_layout(margin=dict(t=25, r=0, l=0, b=0))

    if 1 in checklist and len(values_dict) > 1:
        for curr in list(values_dict.keys()):
            graph.add_trace(
                go.Scatter(x=days_range, y=values_dict[curr],
                           marker=dict(color=color_dict[curr]), name=curr))

    if 2 in checklist:
        graph.update_layout(yaxis=dict(range=[0, 1.1*max(values)]))

    if 3 in checklist:
        inflation_rates = pickle.load(open("inflation_rates.pickle", "rb"))
        values_inf = calculate_inflation(values, inflation_rates, days_range)

        graph.add_trace(go.Scatter(y=pd.Series(values_inf),
                                   x=days_range, marker=dict(color="#A9A9A9"),
                                   name="Po inflacji"))

    graph.add_trace(go.Scatter(y=pd.Series(values), x=days_range,
                               marker=dict(color="black"), name="Całość"))

    return graph


def calculate_inflation(values, inflation_rates, days_range):
    # values_inf = [1 * x for x in values]
    # ---
    basket_price = {}
    x = 20
    for y in list(range(2006, 2009)):
        for m in list(range(1, 13)):
            basket_price[(y, m)] = x
            x += 0.3
    print(basket_price)
    # ---
    values_inf = []
    for val, day in zip(values, days_range):

        if day < datetime(year=list(basket_price.keys())[0][0],
                          month=list(basket_price.keys())[0][1], day=1,
                          hour=1, minute=0):
            # before inflation data registration
            values_inf.append(val)
        elif day > datetime(year=list(basket_price.keys())[-1][0],
                            month=list(basket_price.keys())[-1][1], day=1,
                            hour=1, minute=0):
            # after inflation data registration
            values_inf.append(val/(list(basket_price.values()[-1])/basket_price[])))
        else:
            # during inflation data registration
            values_inf.append(val/inflation_rates[(day.year, day.month)])

    return values_inf
