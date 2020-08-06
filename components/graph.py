import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_html_components as html

import pandas as pd
import numpy as np

from constants import *
from components.plot import plot_treemap

def error_message(message):
    return [dbc.Alert(message, dismissable=True, fade=True, className="mt-2")]

def generate(category, filters, splits, settings):

    color_col = settings[0]
    color_scale = settings[1]

    datasets = {
        'Applications': 'data/applied.csv',
        'Admitted Students': 'data/admitted.csv',
        'SIR\'ed Students': 'data/committed.csv'
    }

    splits = [s.replace('split-', '') for s in splits if s is not None]
    if len(splits) == 0: return error_message('Please choose at least one split!')
    # if len(np.unique(splits)) != len(splits): return error_message('Please choose unique splits!')
    
    category = category.replace('filter-', '')
    df = pd.read_csv(datasets[category])
    
    for key, selected in filters.items():
        key = key.replace('filter-', '')
        if selected is not None and len(selected) > 0:
            selected = [s.replace('filter-', '') for s in selected]
            df = df[df[key].isin(selected)]

    if len(df) == 0: return error_message('Your filters are too narrow!')

    fig = plot_treemap(data=df, path=splits, color_col=color_col, color_scale=color_scale)

    return [dcc.Graph(figure=fig)]

def get_graph_div():
    return dbc.Card(
        [dbc.CardBody(
            [
                dbc.Spinner(html.Div(id="graph-output", className="mt-3"))
            ]
        ), 
        html.Hr(),
        html.Div('', id='graph-description', className='text-center'),
        html.Hr(),
        dbc.Button("Generate Graph", id='generate-graph-button', color="dark", className="w-25 mb-3 mt-10 mx-auto"),],
        className="mt-3",
    )