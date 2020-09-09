import plotly.express as px
from datetime import datetime, timedelta

from funcs import *


def backend(time_range, checklist, start_date, end_date, usd_input, eur_input,
            gbp_input, chf_input, checklist2):

    # Exchange rates (left side)
    df = pd.read_csv("../data/exchange_rates_99_20.csv", sep=';',
                     index_col="index")

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
    big_graph.update_layout(margin=dict(t=25, r=0, l=0, b=0))

    if start_date is not None and end_date is not None \
            and any([x not in [None, ""]
                     for x in [usd_input, eur_input, gbp_input, chf_input]]):

        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        days_elapsed = (end_date - start_date).days
        days_range = [start_date + timedelta(days=x)
                      for x in range(days_elapsed+1)]

        curr_list = [usd_input, eur_input, gbp_input, chf_input]
        curr_dict = {0: "USD", 1: "EUR", 2: "GBP", 3: "CHF"}
        values = [0 for x in days_range]
        values_dict = dict()
        for curr_id, amount in zip(
                [x for x, y in enumerate(curr_list) if y not in [None, ""]],
                [y for x, y in enumerate(curr_list) if y not in [None, ""]]):

            values_dict[curr_dict[curr_id]] = []
            for d, day in enumerate(days_range):
                dt = datetime(year=day.year, month=day.month, day=day.day,
                              hour=1, minute=0, second=0)
                price \
                    = df[curr_dict[curr_id]+"-PLN"].loc[dt.strftime(
                        "%d.%m.%Y %H:%M")]
                values[d] += float(amount)*price
                values_dict[curr_dict[curr_id]].append(float(amount)*price)

        big_graph = draw_big_plot(days_range, values, values_dict, checklist2)

    return [usd_graph, eur_graph, gbp_graph, chf_graph, big_graph]
