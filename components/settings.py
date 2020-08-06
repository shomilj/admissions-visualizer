import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_html_components as html

from constants import *

def generate_options(options):
    return [{"label": o, "value": o} for o in options]

def get_settings_div():
    return dbc.Card(
        dbc.CardBody([
            dbc.FormGroup([
                dbc.Alert(["You can choose to color your graphs by either Headcount or Admit Rate. To view all the color scales available, use ", html.A("this guide.", href="https://plotly.com/python/builtin-colorscales/", className="alert-link")], dismissable=True, fade=True, className="mt-2"),
                dbc.Label('Color Metric', html_for="dropdown", className="mt-3"),
                dcc.Dropdown(id='settings-color-metric', options=generate_options(['Headcount', 'Admit Rate']), value='Headcount'),

                dbc.Label('Color Scale', html_for="dropdown", className="mt-3"),
                dcc.Dropdown(id='settings-color-scale', options=generate_options(COLOR_SCALES), value='greens')                
            ])
        ])
    )