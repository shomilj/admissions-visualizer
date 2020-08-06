import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_html_components as html

from constants import *

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Submit Feedback", href="https://airtable.com/shrS3FkeqE4I2GJ5g"))
    ],
    brand="UC Berkeley Admissions - Data Visualization", brand_href="#", color=PRIMARY_COLOR, dark=True,
)

intro = dbc.Alert(
    ["Welcome! This is an experimental project created to identify trends in UC Berkeley admissions data. To understand what this tool can do, you might want to read ", html.A("this article.", href="https://shomil.me/eecs-diversity", className="alert-link")],
    id="alert-no-fade",
    dismissable=True,
    fade=False,
    is_open=True,
    color="secondary",
    className="mt-4"
)