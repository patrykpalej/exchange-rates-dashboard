import dash
import pandas as pd
import plotly.express as px
from datetime import datetime
import matplotlib.pyplot as plt
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from funcs import *
from layout import frontend
from logic import backend


app = dash.Dash(__name__)

app.layout = frontend()


@app.callback(
     [Output(component_id='usd_graph', component_property='figure'),
      Output(component_id='eur_graph', component_property='figure'),
      Output(component_id='gbp_graph', component_property='figure'),
      Output(component_id='chf_graph', component_property='figure'),
      Output(component_id='big_graph', component_property='figure')],

     [Input(component_id='select_time_range', component_property='value'),
      Input(component_id="checklist", component_property="value"),
      Input(component_id='date_picker', component_property='start_date'),
      Input(component_id='date_picker', component_property='end_date'),
      Input(component_id='usd_input', component_property='value'),
      Input(component_id='eur_input', component_property='value'),
      Input(component_id='gbp_input', component_property='value'),
      Input(component_id='chf_input', component_property='value'),
      Input(component_id="checklist2", component_property="value")]
)
def update_graphs(time_range, checklist, start_date, end_date,
                  usd_input, eur_input, gbp_input, chf_input, checklist2):

    usd_graph, eur_graph, gbp_graph, chf_graph, big_graph \
        = backend(time_range, checklist, start_date, end_date,
                  usd_input, eur_input, gbp_input, chf_input, checklist2)

    return [usd_graph, eur_graph, gbp_graph, chf_graph, big_graph]


if __name__ == '__main__':
    app.run_server(debug=True)
