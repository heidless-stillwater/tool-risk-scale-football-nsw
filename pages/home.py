from dash import html, dcc, Output, Input, State, callback
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash.exceptions import PreventUpdate
from my_app.charts import heatmap_chart_tmp, hss_trend, hss_palette, hss_gauge
import dash
import pandas as pd

dash.register_page(__name__, path="/")


layout = dbc.Container(
    children=[
        html.Div(id="map-component"),
        dbc.Alert(
            [
                html.H3(
                    "The current HSS value is:",
                ),
                dcc.Loading(
                    html.H1(className="alert-heading", id="value-hss-current"),
                    style={"height": "40px"},
                ),
                # html.P("This is a placeholder describing the HSS value"),
                html.Hr(),
                html.H5(
                    "Advisory for the general public regarding activities outdoors: ",
                ),
                html.P(
                    "Healthy persons: Normal activities. ",
                    className="mb-0",
                ),
                html.P(
                    "Elderly, pregnant women, children: Normal activities.",
                    className="mb-0",
                ),
                html.P(
                    "People with lung or heart diseases: Normal activities.",
                    className="mb-0",
                ),
            ],
            className="mt-1",
            id="alert-hss-current",
        ),
        html.H2("HSS forecast"),
        html.Div(id="fig-hss-trend"),
        html.H2("HSS forecast"),
        html.Div(id="fig-forecast"),
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
    Output("fig-forecast", "children"),
    Input("session-storage-weather", "modified_timestamp"),
    State("session-storage-weather", "data"),
)
def update_fig_forecast(ts, data):
    try:
        df = pd.read_json(data, orient="split")
        return dcc.Graph(figure=heatmap_chart_tmp(df))
    except ValueError:
        raise PreventUpdate


@callback(
    Output("fig-hss-trend", "children"),
    Input("session-storage-weather", "modified_timestamp"),
    State("session-storage-weather", "data"),
)
def update_fig_hss_trend(ts, data):
    try:
        df = pd.read_json(data, orient="split")
        return dcc.Graph(figure=hss_gauge(df))
    except ValueError:
        raise PreventUpdate


@callback(
    Output("value-hss-current", "children"),
    Output("alert-hss-current", "color"),
    Input("session-storage-weather", "modified_timestamp"),
    State("session-storage-weather", "data"),
)
def update_alert_hss_current(ts, data):
    try:
        df = pd.read_json(data, orient="split")
        color = hss_palette[df["hss"][0]]
        return f"{df['hss'][0]} - {df['hss_set'][0]}", color
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
