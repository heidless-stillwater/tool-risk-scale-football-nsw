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

from utils import calculate_comfort_indices, get_yr_weather

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


app.layout = html.Div(
    children=[
        dcc.Store(id="local-storage-location", storage_type="local"),
        dcc.Store(id="local-storage-settings", storage_type="local"),
        dcc.Store(id="session-storage-weather", storage_type="session"),
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
    State("session-storage-weather", "modified_timestamp"),
)
def calculated_comfort_indexes(ts, data_location, data_weather_ts):
    if ts is None:
        raise PreventUpdate

    if data_weather_ts != -1 and ((time.time() * 1000 - ts) / 1000) < 5 * 60:
        raise PreventUpdate

    print(f"{datetime.now()} getting comfort indices")
    df = get_yr_weather(
        lat=round(data_location["lat"], 3), lon=round(data_location["lon"], 3)
    )
    df = calculate_comfort_indices(df)

    return df.to_json(date_format="iso", orient="table")


if __name__ == "__main__":
    app.run_server(
        debug=os.environ.get("DEBUG_DASH", True),
        host="0.0.0.0",
        port=8080,
        processes=1,
        threaded=True,
    )
