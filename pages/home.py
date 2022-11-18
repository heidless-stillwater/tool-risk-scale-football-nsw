from dash import html, dcc, Output, Input, State, callback
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash.exceptions import PreventUpdate
from my_app.charts import hss_palette, risk_map
import dash
import pandas as pd

from utils import sma_risk_messages

dash.register_page(__name__, path="/")


layout = dbc.Container(
    children=[
        html.Div(id="map-component"),
        dbc.Alert(
            [
                html.H3(
                    "The current Sport Risk Value:",
                ),
                dcc.Loading(
                    html.H1(className="alert-heading", id="value-hss-current"),
                    style={"height": "40px"},
                ),
                html.P(
                    id="value-risk-description",
                ),
                html.Hr(),
                html.H5(
                    "Suggestions: ",
                ),
                dcc.Markdown(
                    id="value-risk-suggestions",
                    className="mb-0",
                ),
            ],
            className="mt-1",
            id="alert-hss-current",
        ),
        html.H2("Risk value (next 20 hours)"),
        html.Div(id="fig-hss-trend"),
    ],
    className="p-2",
)


@callback(
    Output("local-storage-location", "data"),
    Input("map", "location_lat_lon_acc"),
    State("local-storage-location", "data"),
)
def update_location_and_forecast(location, data):
    data = data or {"lat": 0, "lon": 0}

    if location:
        data["lat"] = location[0]
        data["lon"] = location[1]

    return data


@callback(
    Output("fig-hss-trend", "children"),
    Input("session-storage-weather", "modified_timestamp"),
    State("session-storage-weather", "data"),
)
def update_fig_hss_trend(ts, data):
    try:
        df = pd.read_json(data, orient="table")
        return dcc.Graph(figure=risk_map(df))
    except ValueError:
        raise PreventUpdate


@callback(
    Output("value-hss-current", "children"),
    Output("alert-hss-current", "color"),
    Output("value-risk-description", "children"),
    Output("value-risk-suggestions", "children"),
    Input("session-storage-weather", "modified_timestamp"),
    State("session-storage-weather", "data"),
)
def update_alert_hss_current(ts, data):
    try:
        df = pd.read_json(data, orient="table")
        color = hss_palette[df["risk_value"][0]]
        description = sma_risk_messages[df["risk"][0]]["description"].capitalize()
        suggestion = sma_risk_messages[df["risk"][0]]["suggestions"].capitalize()
        return f"{df['risk'][0]}".capitalize(), color, description, suggestion
    except ValueError:
        raise PreventUpdate


@callback(
    Output("map-component", "children"),
    Input("local-storage-location", "modified_timestamp"),
    State("local-storage-location", "data"),
)
def on_location_change(ts, data):
    if ts is None:
        raise PreventUpdate

    data = data or {"lat": 0, "lon": 0}
    return dl.Map(
        [
            dl.TileLayer(maxZoom=13, minZoom=9),
            dl.LocateControl(
                startDirectly=True,
                options={"locateOptions": {"enableHighAccuracy": True}},
            ),
        ],
        id="map",
        style={
            "width": "100%",
            "height": "25vh",
            "margin": "auto",
            "display": "block",
            # "-webkit-filter": "grayscale(100%)",
            # "filter": "grayscale(100%)",
        },
        center=(data["lat"], data["lon"]),
        zoom=13,
    )
