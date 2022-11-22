from dash import html, dcc, Input, Output, callback, State, ctx
import dash
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from copy import deepcopy
from utils import sports_category

dash.register_page(__name__)


# from https://www.health.vic.gov.au/environmental-health/extreme-heat-information-for-clinicians
questions = [
    {
        "id": "id-class",
        "question": "Please select a sport:",
        "options": list(sports_category.keys()),
        "multi": False,
        "default": [],
    },
]


def generate_dropdown(questions_to_display):
    return [
        dbc.Row(
            [
                html.Label(
                    item["question"],
                    className="py-2",
                ),
                dcc.Dropdown(
                    item["options"], item["default"], multi=item["multi"], id=item["id"]
                ),
            ],
            className="pb-2",
        )
        for item in questions_to_display
    ]


def layout():
    return dbc.Container(
        [dcc.Location(id="url"), html.Div(id="settings-dropdowns")],
        className="p-2",
        style={"min-height": "80vh"},
    )


@callback(
    Output("local-storage-settings", "data"),
    State("local-storage-settings", "data"),
    [Input(question["id"], "value") for question in questions],
)
def update_settings_storage_based_dropdown(data, *args):
    """Saves in local storage the settings selected by the participant"""
    data = data or {}
    for ix, question_id in enumerate([question["id"] for question in questions]):
        data[question_id] = args[ix]

    print(data)
    return data


@callback(
    Output("settings-dropdowns", "children"),
    Input("url", "pathname"),
    State("local-storage-settings", "data"),
)
def display_page(pathname, data):
    if data and pathname == "/settings":
        __questions = deepcopy(questions)
        for ix, q in enumerate(__questions):
            __questions[ix]["default"] = data[q["id"]]
        return generate_dropdown(__questions)
    elif data is None:
        return generate_dropdown(questions)
    else:
        raise PreventUpdate
