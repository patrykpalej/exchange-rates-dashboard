import dash
import pandas as pd
import plotly.express as px
from datetime import datetime
import matplotlib.pyplot as plt
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Kursy walut', style={"text-align": "center"}),

    dcc.Dropdown(id="select_time_range", options=[
                     {"label": "1 miesiąc", "value": 1},
                     {"label": "1 rok", "value": 2},
                     {"label": "5 lat", "value": 3}],
                 style={"width": "30%", "position": "absolute",
                        "left": "18%"}),

    html.Div([
        dcc.Graph(style={"width": "20%", "height": "25%",
                         "position": "absolute", "top": "5%"},
                  id="usd_graph", figure={}),

        dcc.Graph(style={"width": "20%", "height": "25%",
                         "position": "absolute", "top": "30%"}, id="eur_graph"),

        dcc.Graph(style={"width": "20%", "height": "25%",
                         "position": "absolute", "top": "55%"}, id="gbp_graph"),

        dcc.Graph(style={"width": "20%", "height": "25%",
                         "position": "absolute", "top": "80%"}, id="chf_graph"),
    ], style={"height": "90%", "margin-top": "2%"}),


    html.Div([
        dcc.Input(id="usd_input", type="text", placeholder="USD",
                  style={"height": "20px", "width": "150px"}),

        dcc.Input(id="eur_input", type="text", placeholder="EUR",
                  style={"height": "20px", "width": "150px"}),

        dcc.Input(id="gbp_input", type="text", placeholder="GBP",
                  style={"height": "20px", "width": "150px"}),

        dcc.Input(id="chf_input", type="text", placeholder="CHF",
                  style={"height": "20px", "width": "150px"})
    ], style={"display": "grid", "grid-row-gap": "20px",
              "position": "absolute", "top": "15%", "right": "35%"}),

    dcc.DatePickerRange(id='date_picker', display_format="DD-MM-YYYY",
                        min_date_allowed=datetime(2000, 1, 1),
                        max_date_allowed=datetime.now(),
                        style={"top": "15%", "right": "5%",
                               "position": "absolute"}),

    html.Button("Oblicz",
                style={"width": "150px", "position": "absolute", "top": "30%",
                       "right": "10%", "height": "30px"}),

    dcc.Graph(style={"width": "50%", "height": "65%", "position": "absolute",
                     "left": "40%", "top": "40%"}, id="big_graph", figure={})

    ])


@app.callback(
     [Output(component_id='usd_graph', component_property='figure'),
      Output(component_id='eur_graph', component_property='figure'),
      Output(component_id='gbp_graph', component_property='figure'),
      Output(component_id='chf_graph', component_property='figure'),
      Output(component_id='big_graph', component_property='figure')],

    [Input(component_id='select_time_range', component_property='value'),
     Input(component_id='usd_input', component_property='value'),
     Input(component_id='eur_input', component_property='value'),
     Input(component_id='gbp_input', component_property='value'),
     Input(component_id='chf_input', component_property='value'),
     Input(component_id='date_picker', component_property='start_date'),
     Input(component_id='date_picker', component_property='end_date')]
)
def update_graph(time_range, usd_input, eur_input, gbp_input, chf_input,
                 start_date, end_date):
    df1 = pd.read_csv("exchange_rates_99_20.csv", sep=';')

    df = pd.read_csv("intro_bees.csv")
    dff = df.copy()
    dff = dff[dff["Year"] == 2017]
    dff = dff[dff["Affected by"] == "Varroa_mites"]

    # df = px.data.gapminder().query("country=='Canada'")
    # usd_graph = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')

    usd_graph \
        = px.line(df1, x='timestamp', y='USD-PLN')
    eur_graph \
        = px.line(df1, x='timestamp', y='EUR-PLN')
    gbp_graph \
        = px.line(df1, y='GBP-PLN')
    chf_graph \
        = px.line(df1, y='CHF-PLN')

    big_graph \
        = px.line(dff, x='Pct of Colonies Impacted',
                  y='Pct of Colonies Impacted')

    # eur_graph = plt.figure()
    # gbp_graph = plt.figure()
    # chf_graph = plt.figure()
    # big_graph = plt.figure()

    return [usd_graph, eur_graph, gbp_graph, chf_graph, big_graph]


if __name__ == '__main__':
    app.run_server(debug=True)