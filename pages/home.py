import os

from dash import html, dcc, Output, Input, State, callback, ctx
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash.exceptions import PreventUpdate
from my_app.charts import hss_palette, risk_map, indicator_chart
import dash
import pandas as pd
from utils import sma_risk_messages, sports_category, legend_risk


dash.register_page(
    __name__,
    path="/",
    title="Home Page",
    name="Home Page",
    description="This is the home page of the SMA Extreme Policy Tool",
)


def layout():
    return dbc.Container(
        children=[
            html.Div(id="map-component"),
            html.Div(id="body-home"),
        ],
        className="p-2",
    )


@callback(
    Output("body-home", "children"),
    Input("local-storage-settings", "data"),
)
def body(data):
    try:
        sport_selected = data["id-class"]
        if not sport_selected:
            return [
                dbc.Alert(
                    "Please return to the Settings Page and select a sport",
                    id="sport-selection",
                    color="danger",
                    className="mt-2",
                ),
                html.Div(
                    [
                        dbc.Button("Settings Page", color="primary", href="/settings"),
                    ],
                    className="d-grid gap-2 col-4 mx-auto",
                ),
            ]
        else:
            return [
                dbc.Row(
                    html.Div(
                        id="id-icon-sport",
                        className="p-2",
                    ),
                    justify="center",
                ),
                dbc.Row(
                    dbc.Col(
                        [
                            html.H3(
                                "The current Heat Stress Risk:",
                            ),
                            dcc.Loading(
                                html.H1(
                                    className="alert-heading",
                                    id="value-hss-current",
                                ),
                            ),
                        ],
                        style={"text-align": "center"},
                    ),
                ),
                html.Div(id="fig-indicator"),
                legend_risk(),
                dbc.Alert(
                    [
                        # html.Hr(),
                        html.Div(id="div-icons-suggestions"),
                    ],
                    className="mt-1",
                    id="id-alert-risk-current",
                ),
                dbc.Accordion(
                    dbc.AccordionItem(
                        [
                            html.P(
                                id="value-risk-description",
                            ),
                            html.P(
                                "You should:",
                            ),
                            dcc.Markdown(
                                id="value-risk-suggestions",
                                className="mb-0",
                            ),
                        ],
                        title="Detailed suggestions: ",
                    ),
                    start_collapsed=True,
                    className="my-2",
                    id="id-accordion-risk-current",
                ),
                html.H2("Risk value trend in the next 20 hours"),
                html.Div(id="fig-hss-trend"),
                legend_risk(),
            ]
    except:
        return [
            dbc.Alert(
                "Please select a sport in the Settings Page",
                id="sport-selection",
                color="danger",
                className="mt-2",
            ),
            html.Div(
                [
                    dbc.Button(
                        "Go to the Settings Page", color="primary", href="/settings"
                    ),
                ],
                className="d-grid gap-2 col-4 mx-auto",
            ),
        ]


def icon_component(src, message, size="50px"):
    return dbc.Row(
        [
            dbc.Col(
                html.Img(src=src, width=size),
                style={"text-align": "right"},
                width="auto",
            ),
            dbc.Col(
                message,
                width="auto",
                style={"text-align": "left"},
            ),
        ],
        align="center",
        justify="center",
        className="my-1",
    )


@callback(
    Output("local-storage-location-gps", "data"),
    Input("map", "location_lat_lon_acc"),
    State("local-storage-location-gps", "data"),
)
def update_location_and_forecast(location, data):
    data = data or {"lat": -33.888, "lon": 151.185}

    if location:
        data["lat"] = location[0]
        data["lon"] = location[1]

    return data


@callback(
    Output("id-icon-sport", "children"),
    Input("local-storage-settings", "data"),
)
def update_location_and_forecast(data_sport):

    try:
        file_name = f"{data_sport['id-class']}.png"
    except KeyError:
        raise PreventUpdate
    path = os.path.join(os.getcwd(), "assets", "icons", file_name)
    # source https://www.theolympicdesign.com/olympic-design/pictograms/tokyo-2020/
    if os.path.isfile(path):
        return icon_component(
            f"../assets/icons/{data_sport['id-class']}.png", data_sport["id-class"]
        )
    else:
        return icon_component("../assets/icons/sports.png", data_sport["id-class"])


@callback(
    Output("fig-hss-trend", "children"),
    Input("session-storage-weather", "modified_timestamp"),
    State("session-storage-weather", "data"),
    State("local-storage-settings", "data"),
)
def update_fig_hss_trend(ts, data, data_sport):
    try:
        df = pd.read_json(data, orient="table")
        return dcc.Graph(
            figure=risk_map(df, sports_category[data_sport["id-class"]]),
            config={"staticPlot": True},
        )
    except ValueError:
        raise PreventUpdate


@callback(
    Output("fig-indicator", "children"),
    Input("session-storage-weather", "modified_timestamp"),
    State("session-storage-weather", "data"),
    State("local-storage-settings", "data"),
)
def update_fig_hss_trend(ts, data, data_sport):
    try:
        df = pd.read_json(data, orient="table")
        return dcc.Graph(
            figure=indicator_chart(df, sports_category[data_sport["id-class"]]),
            config={"staticPlot": True},
        )
    except ValueError:
        raise PreventUpdate


@callback(
    Output("value-hss-current", "children"),
    Output("id-alert-risk-current", "color"),
    Output("value-risk-description", "children"),
    Output("value-risk-suggestions", "children"),
    Output("div-icons-suggestions", "children"),
    Input("session-storage-weather", "modified_timestamp"),
    State("session-storage-weather", "data"),
)
def update_alert_hss_current(ts, data):
    try:
        df = pd.read_json(data, orient="table")
        color = hss_palette[df["risk_value"][0]]
        risk_class = df["risk"].iloc[0]
        description = sma_risk_messages[risk_class]["description"].capitalize()
        suggestion = sma_risk_messages[risk_class]["suggestions"].capitalize()
        icons = [
            icon_component("../assets/icons/water-bottle.png", "Stay hydrated"),
            icon_component("../assets/icons/tshirt.png", "Wear light clothing"),
        ]
        if risk_class == "moderate":
            icons.append(
                icon_component("../assets/icons/pause.png", "Rest Breaks"),
            )
        if risk_class == "high":
            icons.append(
                icon_component("../assets/icons/pause.png", "Rest Breaks"),
            )
            icons.append(
                icon_component("../assets/icons/slush-drink.png", "Active Cooling"),
            )
        if risk_class == "extreme":
            icons = [
                icon_component(
                    "../assets/icons/stop.png", "Stop Activity", size="100px"
                ),
            ]
        return f"{risk_class}".capitalize(), color, description, suggestion, icons
    except ValueError:
        raise PreventUpdate


@callback(
    Output("map-component", "children"),
    Input("local-storage-location-gps", "modified_timestamp"),
    Input("local-storage-location-selected", "modified_timestamp"),
    State("local-storage-location-gps", "data"),
    State("local-storage-location-selected", "data"),
)
def on_location_change(ts_gps, ts_selected, loc_gps, loc_selected):

    start_location_control = True
    if loc_gps or loc_selected:
        start_location_control = False

    loc_gps = loc_gps or {"lat": -0, "lon": 0}

    if ctx.triggered_id != "local-storage-location-gps" and loc_selected:
        loc_gps = loc_selected

    return dl.Map(
        [
            dl.TileLayer(maxZoom=13, minZoom=9),
            dl.LocateControl(
                startDirectly=start_location_control,
                options={"locateOptions": {"enableHighAccuracy": True}},
            ),
            dl.Marker(position=[loc_gps["lat"], loc_gps["lon"]]),
            dl.GestureHandling(),
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
        center=(loc_gps["lat"], loc_gps["lon"]),
        zoom=13,
    )
