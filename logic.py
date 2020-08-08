import dash
import pandas as pd
import plotly.express as px
from datetime import datetime
import matplotlib.pyplot as plt
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from funcs import *


def backend(time_range, checklist, usd_input, eur_input, gbp_input, chf_input,
            start_date, end_date):

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
    dfff = pd.read_csv("intro_bees.csv")
    dff = dfff.copy()
    dff = dff[dff["Year"] == 2017]
    dff = dff[dff["Affected by"] == "Varroa_mites"]

    big_graph \
        = px.line(dff, x='Pct of Colonies Impacted',
                  y='Pct of Colonies Impacted')

    return [usd_graph, eur_graph, gbp_graph, chf_graph, big_graph]
