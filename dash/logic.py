import dash
import pandas as pd
import plotly.express as px
from datetime import datetime
import matplotlib.pyplot as plt
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from funcs import *


def backend(time_range, checklist, start_date, end_date, n_clicks,
            usd_input, eur_input, gbp_input, chf_input):

    # Exchange rates (left side)
    df = pd.read_csv("exchange_rates_99_20.csv", sep=';')

    usd_graph \
        = draw_plot(df, col="USD-PLN",
                    cols_list=["USD-EUR", "USD-GBP", "USD-CHF"],
                    second_label="USD (EUR, GBP, CHF)", time_range=time_range,
                    plot_types=checklist)

    eur_graph \
        = draw_plot(df, col="EUR-PLN",
                    cols_list=["EUR-USD", "EUR-GBP", "EUR-CHF"],
                    second_label="EUR (USD, GBP, CHF)", time_range=time_range,
                    plot_types=checklist)

    gbp_graph \
        = draw_plot(df, col="GBP-PLN",
                    cols_list=["GBP-USD", "GBP-EUR", "GBP-CHF"],
                    second_label="GBP (USD, EUR, CHF)", time_range=time_range,
                    plot_types=checklist)

    chf_graph \
        = draw_plot(df, col="CHF-PLN",
                    cols_list=["CHF-USD", "CHF-EUR", "CHF-GBP"],
                    second_label="CHF (USD, EUR, GBP)", time_range=time_range,
                    plot_types=checklist)

    # Value variation over time (right side)
    big_graph = px.line()

    if usd_input is None and eur_input is None and gbp_input is None \
            and chf_input is None:
        pass
    else:
        big_graph = px.line([usd_input, eur_input], [gbp_input, chf_input])

    # big_graph = px.line()
    print(n_clicks)

    return [usd_graph, eur_graph, gbp_graph, chf_graph, big_graph]
