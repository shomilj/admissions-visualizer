import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_html_components as html

import data

from constants import *

def generate_split(id, title, value, options, multi, description=None):
    return [
        dbc.Label(title, html_for="dropdown", className="mt-3"),
        html.Br() if description is not None else None,
        dbc.Label(description, html_for="dropdown", color='secondary'),
        dcc.Dropdown(id=id, multi=multi, options=[{"label": x, "value": f"split-{x}"} for x in options], value=value)
    ]

filter_options = list(sorted(data.load_columns().keys()))

splits = []
for i in range(NUM_SPLITS):
    if i == 0: value = 'split-Gender'
    elif i == 1: value = 'split-Intended Major'
    else: value = None
    splits.extend(generate_split(id=f'split-{i}', title=f'Level {i}', value=value, options=filter_options, multi=False))

def get_split_div():
    return dbc.Card(
        dbc.CardBody([
            dbc.Alert("First, choose a few splitting values. Recommended: leave the default values for now!", dismissable=True, fade=True, className="mt-2"),
            dbc.FormGroup(
                splits
            )
        ]), className="mt-3"
    )