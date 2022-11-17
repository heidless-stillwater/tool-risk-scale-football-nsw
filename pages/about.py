import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__)

body_text = """
# About Heat Stress Scale (HSS)

## Definition and aim

The Heat Stress Scale (HSS) aims at enhancing community resilience to heatwave disasters. 
The HSS consists of stratified risk categories (numbered 0 to 5, with 1 decimal place). 
The highest the number the worse the condition is.

## More about the scale
The HSS will provide a simple interpretation of the current and forecasted heat stress risk by
integrating not only temperature (typically used by the public to assess risk), but also humidity,
solar radiation, and wind speed. These parameters will be derived from freely available online
weather reports/forecasts (e.g., BOM) and integrated using a physiological human
thermoregulation model that estimates the risk of overheating and dehydration and associated
negative health effects.
"""

layout = dbc.Container(
    dcc.Markdown(body_text),
    className="p-2",
)
