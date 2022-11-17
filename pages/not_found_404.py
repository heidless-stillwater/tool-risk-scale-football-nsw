from dash import html
import dash
import dash_bootstrap_components as dbc

dash.register_page(__name__)

layout = dbc.Container(html.H1("This is our custom 404 content"))
