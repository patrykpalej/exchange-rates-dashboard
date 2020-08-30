from datetime import datetime
import dash_core_components as dcc
import dash_html_components as html


def frontend():
    layout_ = html.Div([
        html.H1("Kursy walut",
                style={"text-align": "center", "fontSize": "50px",
                       "margin": "0"}),

        html.H2("Opcje wizualizacji", style={"top": "18%", "left": "40%",
                                             "position": "absolute"}),

        dcc.RadioItems(id="select_time_range", options=[
            {"label": "1 miesiąc", "value": 1},
            {"label": "1 rok", "value": 2},
            {"label": "5 lat", "value": 3},
            {"label": "Cały przedział", "value": 4}], value=2,
                       style={"width": "10%", "position": "absolute",
                              "display": "grid", "left": "40%", "top": "25%",
                              "height": "12%"}),

        dcc.Checklist(id="checklist", value=[1], options=[
            {"label": "Cena w PLN", "value": 1},
            {"label": "Średnia cena we wszystkich walutach", "value": 2}],
                      style={"width": "10%", "position": "absolute",
                             "display": "grid", "left": "40%", "top": "45%",
                             "height": "12%"}),

        html.Div([
            dcc.Graph(style={"width": "39%", "height": "26%",
                             "position": "absolute", "top": "0%"},
                      id="usd_graph"),

            dcc.Graph(style={"width": "39%", "height": "26%",
                             "position": "absolute", "top": "25%"},
                      id="eur_graph"),

            dcc.Graph(style={"width": "39%", "height": "26%",
                             "position": "absolute", "top": "50%"},
                      id="gbp_graph"),

            dcc.Graph(style={"width": "39%", "height": "26%",
                             "position": "absolute", "top": "75%"},
                      id="chf_graph"),
        ], style={"height": "90%", "margin-top": "2%", "left": "0"}),

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
                  "position": "absolute", "top": "12%", "right": "30%"}),

        dcc.DatePickerRange(id="date_picker", display_format="DD-MM-YYYY",
                            min_date_allowed=datetime(2000, 1, 1),
                            max_date_allowed=datetime.now(),
                            style={"top": "12%", "right": "5%",
                                   "position": "absolute"}),

        dcc.Checklist(id="checklist2", value=[1], options=[
            {"label": "Pokaż wykresy cząstkowe", "value": 1},
            {"label": "Pokaż linie trendu", "value": 2},
            {"label": "Wartości na osi Y od 0", "value": 3},
            {"label": "Uwzględnij inflację (2006-2019)", "value": 4}],
                      style={"width": "20%", "position": "absolute",
                             "display": "grid", "left": "78%", "top": "22%",
                             "height": "13%"}),

        dcc.Graph(
            style={"width": "49%", "height": "60%", "position": "absolute",
                   "left": "50%", "top": "37%"}, id="big_graph", figure={})
    ])

    return layout_
