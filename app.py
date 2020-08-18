import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import data
from components import filters, splits, home, graph, settings, barchart

import plotly.express as px
import pandas as pd

from constants import *

external_scripts = [
    'https://www.googletagmanager.com/gtag/js?id=UA-148444994-1',
    'assets/analytics.js'
]

app = dash.Dash(__name__, external_scripts=external_scripts, external_stylesheets=[dbc.themes.BOOTSTRAP], title='Berkeley Admissions', update_title='')

server = app.server

# We have two categories: "Filter", and "Group By".

app.layout = html.Div(children=[
    html.Script(GOOGLE_ANALYTICS_SCRIPT),
    home.navbar,
    html.Div([
        home.intro,
        dbc.Tabs([
            dbc.Tab(splits.get_split_div(), label='Splits'),
            dbc.Tab(filters.get_filter_div(), label='Filters'),
            dbc.Tab(graph.get_graph_div(), label='Tree Map'),
            dbc.Tab(barchart.get_bar_div(), label='Bar Chart'),
            dbc.Tab(settings.get_settings_div(), label='Graph Settings'),
        ])
    ], className="container")
])

@app.callback(
    [Output("graph-output", "children"), Output("graph-description", "children")], 
    [Input("generate-graph-button", "n_clicks")] + \
        [Input("filter-" + col, "value") for col in sorted(data.load_columns().keys())] + \
        [Input(f"split-{i}", "value") for i in range(NUM_SPLITS)] + \
        [Input("treemap-color-metric", "value"), Input("treemap-color-scale", "value")]
)
def on_generate_graph(n, *argv):

    filters, splits, children = preprocess(argv)
    alert = dbc.Alert("When you're ready, hit the generate button below. If you change your splits/filters, you'll have to re-generate your graph.", dismissable=True, fade=True, className="mt-2"),
    if not dash.callback_context.triggered[0]['prop_id'].split('.')[0] == 'generate-graph-button':
        return alert, children

    settings = argv[-2:]
    color_col = settings[0]
    color_scale = settings[1]

    return graph.generate(filters, splits, color_col, color_scale), children


@app.callback(
    [Output("barchart-output", "children"), Output("barchart-description", "children")], 
    [Input("generate-barchart-button", "n_clicks")] + \
        [Input("filter-" + col, "value") for col in sorted(data.load_columns().keys())] + \
        [Input(f"split-{i}", "value") for i in range(NUM_SPLITS)] + \
        [Input("barchart-y-axis", "value")]
)
def on_generate_barchart(n, *argv):

    filters, splits, children = preprocess(argv)
    alert = dbc.Alert("To use the bar chart, choose one or two splitting values and filter your data. Then, hit the Generate button below!", dismissable=True, fade=True, className="mt-2"),
    if not dash.callback_context.triggered[0]['prop_id'].split('.')[0] == 'generate-barchart-button':
        return alert, children

    settings = argv[-1:]
    y_axis = settings[0]

    return barchart.generate(filters, splits, y_axis), children

def preprocess(argv):
    filters = []
    splits = []

    i = 0
    for col in sorted(data.load_columns().keys()):
        values = argv[i]
        if values is not None and len(values) > 0:
            filters.extend([
                html.I(', '.join([v.replace('filter-', '') for v in values])),
                html.Br()
            ])
        i += 1

    for _ in range(NUM_SPLITS):
        if argv[i] is not None:
            splits.append(html.I(argv[i].replace('split-', '')))
            splits.append(html.Br())
        i += 1
    
    children = []
    children.append(html.H5('Filters'))
    children.extend(filters)
    children.append(html.H5('Splits', className='mt-3'))
    children.extend(splits)

    i = 0
    filters = {}
    splits = []

    filter_values = []

    # One filter for each column
    for col in sorted(data.load_columns().keys()):
        filters[col] = argv[i]
        i += 1

    # The rest of the arguments are splits.    
    for _ in range(NUM_SPLITS):
        splits.append(argv[i])
        i += 1


    return filters, splits, children


if __name__ == '__main__':
    app.run_server(debug=True)
