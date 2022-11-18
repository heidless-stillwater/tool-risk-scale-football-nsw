import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__)

body_text = """
# Extreme Heat Policy

## Scope
This website in its current form provides recommendations only for Category 3 sports as defined in the 
Extreme Heat Policy v1.0 2021, issued by Sport Medicine Australia. Sports in Risk Classification 3 are: 
* Abseiling
* Australian Football
* Basketball
* Cycling
* Canoeing
* Caving
* Kayaking
* Netball
* Oztag
* Rock Climbing
* Rowing
* Soccer
* Tennis
* Touch Football
* Long Distance Running
* Triathlon
* Volleyball

## Introduction

The new SMA Extreme Heat Policy utilises the latest published research evidence to inform a) a
biophysical model for predicting heat stress risk; and b) recommended cooling strategies that
can be used to optimally mitigate heat stress risk. The new policy also adopts a continuous
approach to defining heat stress risk thresholds in place of stepwise categories and covers gaps
in the previous policy for conditions that often occur in many states and territories that are very
hot (35-40C) but dry (<10%RH), which yield relatively low dew point temperatures yet induce
high levels of sweating and physiological strain, particularly during exercise. A broad
differentiation between the thermal effects of activity levels and clothing/equipment worn
across a range of popular sports in Australia is also provided.

## Aim
The aim of this policy is to provide evidence-based guidance for protecting the health of those
participating in sport and physical activity from the potentially ill effects of extreme heat in the
summer, while ensuring that play is not unnecessarily interrupted. As new research findings
emerge, the policy will be updated accordingly. Intended users are sporting administrators,
coaches and sports medical teams responsible for the safety and wellbeing of people engaging
in sport and physical activity in hot weather, as well as individuals wishing to manage heat
stress risk during planned training activities.

## Disclaimer
The information in this policy is general. Reading or using this policy is not the same as
getting medical advice from your doctor or health professional. All reasonable attempts have
been made to ensure the information is accurate. However, SMA is not responsible for any
loss, injury, claim or damage that may result from using or applying the information in this
policy. The information in this policy should be considered and interpreted in the context of
other risk management, insurance, governance and compliance frameworks and obligations
relevant to sporting organisations. Familiarity with relevant International Sports Federation
(ISF), National Sporting Organisation (NSO) and State Sporting Organisation (SSO) policies
and requirements is essential to enable appropriate interpretation and application of the
information in this policy.
"""

layout = dbc.Container(
    dcc.Markdown(body_text),
    className="p-2",
)
