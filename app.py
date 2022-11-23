import time
from datetime import datetime

from dash import Dash, Input, Output, State
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
    <meta property="og:description" content="The SMA Extreme Heat Policy tool allows you to quickly determine the risk of heath illness based on the type of sport you are playing anf the weather conditions">
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
        dcc.Store(id="local-storage-location", storage_type="local"),
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


@app.callback(
    Output("session-storage-weather", "data"),
    Input("local-storage-location", "modified_timestamp"),
    State("local-storage-location", "data"),
    State("local-storage-settings", "data"),
    State("session-storage-weather", "modified_timestamp"),
)
def calculated_comfort_indexes(ts, data_location, data_sport, data_weather_ts):
    if ts is None:
        raise PreventUpdate

    if data_weather_ts != -1 and ((time.time() * 1000 - ts) / 1000) < 5 * 60:
        raise PreventUpdate

    if not data_sport:
        raise PreventUpdate

    try:
        print(f"{datetime.now()} getting comfort indices")
        df = get_yr_weather(
            lat=round(data_location["lat"], 3), lon=round(data_location["lon"], 3)
        )
        df = calculate_comfort_indices(df, sports_category[data_sport["id-class"]])

        return df.to_json(date_format="iso", orient="table")
    except:
        raise PreventUpdate


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


if __name__ == "__main__":
    app.run_server(
        debug=os.environ.get("DEBUG_DASH", True),
        host="0.0.0.0",
        port=8080,
        processes=1,
        threaded=True,
    )
