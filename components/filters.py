import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_html_components as html

from constants import *

import data

def generate_filter(id, title, options, multi, value=None, clearable=False, description=None):

    # Override for Academic Year.
    if title == 'Academic Yr':
        value = ['filter-2020-21']

    return [
        dbc.Label(title, html_for="dropdown", className="mt-3"),
        html.Br() if description is not None else None,
        dbc.Label(description, html_for="dropdown", color='secondary'),
        dcc.Dropdown(id=id, multi=multi, options=[{"label": x, "value": f"filter-{x}"} for x in options], value=value, clearable=clearable)
    ]

columns = data.load_columns()
filters = []
for col in sorted(columns.keys()):
    values = columns[col]
    filters.extend(generate_filter(id='filter-' + col, title=col, options=values, multi=True))

def get_filter_div():
    return dbc.Card(
        dbc.CardBody([
            dbc.FormGroup(
                [dbc.Alert("Next, filter your data. Recommended: leave the default values for now!", dismissable=True, fade=True, className="mt-2")] + \
                generate_filter(id='category-filter', title='Applications, Acceptances, or SIR\'s', 
                                options=['Applications', 'Admitted Students', 'SIR\'ed Students'], multi=False, clearable=False, value='filter-SIR\'ed Students') + \
                filters
            )
        ])
    )