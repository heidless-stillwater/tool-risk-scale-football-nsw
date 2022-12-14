from dash import Dash, Input, Output, State, ctx
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash import html, dcc
from my_app.navbar import my_navbar
from my_app.footer import my_footer
import os
import dash

from utils import calculate_comfort_indices, get_yr_weather, sports_category

app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
    ],
    prevent_initial_callbacks=True,
    use_pages=True,
)
app.config.suppress_callback_exceptions = True

app.index_string = """<!DOCTYPE html>
<html lang="en-US">
<head>
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-B66DGF5EH0"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-B66DGF5EH0');
    </script>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="author" content="Federico Tartarini, Ollie Jay">
    <meta name="keywords" content="Heat Stress Risk sport, SMA Extreme Heat Policy, Sport Medicine Australia">
    <meta name="description" content="The SMA Extreme Heat Policy tool allows you to quickly determine the risk of heath illness based on the type of sport you are playing anf the weather conditions">
    <title>SMA Extreme Heat Policy Tool</title>
    <meta property="og:image" content="https://github.com/FedericoTartarini/tool-risk-scale-football-nsw/blob/master/assets/icons/HHRI%20logo.png">
    <meta property="og:description" content="The SMA Extreme Heat Policy tool allows you to quickly determine the risk of heath illness based on the type of sport you are playing">
    <meta property="og:title" content="SMA Extreme Heat Policy Tool">
    {%favicon%}
    {%css%}
</head>
<body>
{%app_entry%}
<footer>
{%config%}
{%scripts%}
{%renderer%}
</footer>
</body>
</html>
"""


app.layout = html.Div(
    children=[
        dcc.Location(id="url"),
        dcc.Store(id="local-storage-location-gps", storage_type="local"),
        dcc.Store(id="local-storage-location-selected", storage_type="local"),
        dcc.Store(id="local-storage-settings", storage_type="local"),
        dcc.Store(id="session-storage-weather", storage_type="session"),
        html.Div(id="id-google-analytics-event"),
        my_navbar(),
        html.Div(dash.page_container, style={"flex": 1}),
        my_footer(),
    ],
    style={
        "min-height": "100vh",
        "margin": 0,
        "display": "flex",
        "flex-direction": "column",
    },
)


app.clientside_callback(
    """
    function(pathname, data){
        if (data && pathname === "/"){
            console.log("writing to google analytics");
            return gtag('event', 'sport_selection', {
                                'sport_selected': data["id-class"],
            })
        }
    }
    """,
    Output("id-google-analytics-event", "children"),
    [Input("url", "pathname"), State("local-storage-settings", "data")],
)


@app.callback(
    Output(f"navbar-collapse", "is_open"),
    [Input(f"navbar-toggle", "n_clicks")],
    [State(f"navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(
        debug=os.environ.get("DEBUG_DASH", True),
        host="0.0.0.0",
        port=8080,
        processes=1,
        threaded=True,
    )

# """
# A simple app demonstrating how to manually construct a navbar with a customised
# layout using the Navbar component and the supporting Nav, NavItem, NavLink,
# NavbarBrand, and NavbarToggler components.
#
# Requires dash-bootstrap-components 0.3.0 or later
# """
# import dash
# import dash_bootstrap_components as dbc
# from dash import Input, Output, State, html
#
# PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
#
# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
# # try running the app with one of the Bootswatch themes e.g.
# # app = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL])
# # app = dash.Dash(external_stylesheets=[dbc.themes.SKETCHY])
#
# # make a reuseable navitem for the different examples
# nav_item = dbc.NavItem(dbc.NavLink("Link", href="#"))
#
# # make a reuseable dropdown for the different examples
# dropdown = dbc.DropdownMenu(
#     children=[
#         dbc.DropdownMenuItem("Entry 1"),
#         dbc.DropdownMenuItem("Entry 2"),
#         dbc.DropdownMenuItem(divider=True),
#         dbc.DropdownMenuItem("Entry 3"),
#     ],
#     nav=True,
#     in_navbar=True,
#     label="Menu",
# )
#
#
# # this example that adds a logo to the navbar brand
# logo = dbc.Navbar(
#     dbc.Container(
#         [
#             html.A(
#                 # Use row and col to control vertical alignment of logo / brand
#                 dbc.Row(
#                     [
#                         dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
#                         dbc.Col(dbc.NavbarBrand("Logo", className="ms-2")),
#                     ],
#                     align="center",
#                     className="g-0",
#                 ),
#                 href="https://plotly.com",
#                 style={"textDecoration": "none"},
#             ),
#             dbc.NavbarToggler(id="navbar-toggler2", n_clicks=0),
#             dbc.Collapse(
#                 dbc.Nav(
#                     [nav_item, dropdown],
#                     className="ms-auto",
#                     navbar=True,
#                 ),
#                 id="navbar-collapse2",
#                 navbar=True,
#             ),
#         ],
#     ),
#     color="dark",
#     dark=True,
#     className="mb-5",
# )
#
# app.layout = html.Div([logo])
#
#
# # the same function (toggle_navbar_collapse) is used in all three callbacks
# @app.callback(
#     Output(f"navbar-collapse2", "is_open"),
#     [Input(f"navbar-toggler2", "n_clicks")],
#     [State(f"navbar-collapse2", "is_open")],
# )
# def toggle_navbar_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open
#
#
# if __name__ == "__main__":
#     app.run_server(debug=True, port=8888)
