import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_html_components as html

import pandas as pd
import numpy as np

from constants import *
from components.plot import plot_barchart

def error_message(message):
    return [dbc.Alert(message, dismissable=True, fade=True, className="mt-2")]

def generate(filters, splits, y_axis):

    df = pd.read_csv('data/merged.csv')
    df_all = df.copy()

    splits = [s.replace('split-', '') for s in splits if s is not None]
    if len(splits) == 0: return error_message('Please choose at least one split!')
    if len(splits) > 2: return error_message('Bar charts can only be split on two values at this time!')

    for key, selected in filters.items():
        key = key.replace('filter-', '')
        if selected is not None and len(selected) > 0:
            selected = [s.replace('filter-', '') for s in selected]
            df = df[df[key].isin(selected)]
            if key != 'Segment':
                df_all = df_all[df_all[key].isin(selected)]

    if len(df) == 0: return error_message('Your filters are too narrow!')
    
    fig = plot_barchart(filtered=df, filtered_all=df_all, path=splits, y_axis=y_axis)

    return [dcc.Graph(figure=fig)]

def get_bar_div():
    return dbc.Card(
        [dbc.CardBody(
            [
                dbc.Spinner(html.Div(id="barchart-output", className="mt-3"))
            ]
        ), 
        html.Hr(),
        html.Div('', id='barchart-description', className='text-center'),
        html.Hr(),
        dbc.Button("Generate Barchart", id='generate-barchart-button', color="dark", className="w-25 mb-3 mt-10 mx-auto"),],
        className="mt-3",
    )