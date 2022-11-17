from dash import html, dcc, Input, Output, callback, State, ctx
import dash
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from copy import deepcopy

dash.register_page(__name__)

# from https://www.health.vic.gov.au/environmental-health/extreme-heat-information-for-clinicians
questions = [
    {
        "id": "demo-sex",
        "question": "Sex:",
        "options": [
            "Male",
            "Female",
            "Other",
            "Prefer not to say",
        ],
        "multi": False,
        "default": [],
    },
    {
        "id": "demo-age",
        "question": "Select your age group",
        "options": [
            "< 20",
            "20 - 35",
            "35 - 50",
            "50 - 75",
            "> 75",
        ],
        "multi": False,
        "default": [],
    },
    {
        "id": "demo-activity",
        "question": "Occupation and recreation",
        "options": [
            "Vigorous exercise outdoors",
            "Work outdoors",
        ],
        "multi": True,
        "default": [],
    },
    {
        "id": "demo-illnesses",
        "question": "Chronic illness (select all the applicable)",
        "options": [
            "Heart disease",
            "Diabetes",
            "Hypertension",
            "Cancer",
            "Kidney disease",
            "Substance abuse",
            "Mental illness",
        ],
        "multi": True,
        "default": [],
    },
    {
        "id": "demo-group-risk",
        "question": "Are you in any this groups at greater risk?",
        "options": [
            "people over the age of 65",
            "infants and young children",
            "people who are overweight or obese",
            "pregnant women and breastfeeding mothers",
            "people who have low cardiovascular fitness",
            "people who are not acclimatised to hot weather",
        ],
        "multi": True,
        "default": [],
    },
    {
        "id": "demo-medications",
        "question": "Are you taking any of the following medications?",
        "options": [
            "antibiotics",
            "adrenergic drugs",
            "insulin",
            "analgesics",
            "sedatives",
        ],
        "multi": True,
        "default": [],
    },
    {
        "id": "demo-social-factors",
        "question": "Social factors",
        "options": [
            "live alone or are socially isolated",
            "have a low socioeconomic status",
            "are homeless",
        ],
        "multi": True,
        "default": [],
    },
]


def generate_dropdown(questions_to_display):
    return [
        dbc.Row(
            [
                html.Label(
                    item["question"],
                    className="pb-2",
                ),
                dcc.Dropdown(
                    item["options"], item["default"], multi=item["multi"], id=item["id"]
                ),
            ],
            className="pb-2",
        )
        for item in questions_to_display
    ]


layout = dbc.Container(
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
    return data


@callback(
    Output("settings-dropdowns", "children"),
    Input("url", "pathname"),
    State("local-storage-settings", "data"),
)
def display_page(pathname, data):
    if data and pathname == "/settings":
        print(data)
        __questions = deepcopy(questions)
        for ix, q in enumerate(__questions):
            __questions[ix]["default"] = data[q["id"]]
        return generate_dropdown(__questions)
    elif data is None:
        return generate_dropdown(questions)
    else:
        raise PreventUpdate
