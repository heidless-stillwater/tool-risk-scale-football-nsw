import warnings

import numpy as np

warnings.simplefilter(action="ignore", category=FutureWarning)

import pandas as pd
import requests
import pytz

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    )
}


sma_risk_messages = {
    "low": {
        "description": (
            "maintaining hydration through regular fluid consumption and modifying"
            " clothing is still a simple, yet effective, way of keeping cool and"
            " preserving health and performance during the summer months."
        ),
        "suggestions": """
        * Ensure pre-exercise hydration by consuming 6 ml of water per kilogram of body weight
        every 2-3 hours before exercise. For a 70kg individual, this equates to 420ml of fluid
        every 2-3 hours (a standard sports drink bottle contains 500ml).
        * Drink regularly throughout exercise. You should aim to drink enough to offset sweat
        losses, but it is important to avoid over-drinking because this can also have negative
        health effects. To familiarise yourself with how much you typically sweat, become
        accustomed to weighing yourself before and after practice or competition.
        * Where possible, select light-weight and breathable clothing with extra ventilation.
        * Remove unnecessary clothing/equipment and/or excess clothing layers.
        * Reduce the amount of skin that is covered by clothing – this will help increase your
        sweat evaporation, which will help you dissipate heat.
            """,
    },
    "moderate": {
        "description": (
            "increasing the frequency and/or duration of your rest breaks during"
            " exercise or sporting activities is an effective way of reducing your risk"
            " for heat illness even if minimal resources are available."
        ),
        "suggestions": """
        * During training sessions, provide a minimum of 15 minutes of rest for every 45 minutes
        of practice.
        * Extend scheduled rest breaks that naturally occur during match-play of a particular
        sport (e.g. half-time) by ~10 minutes. This is effective for sports such as soccer/football and
        rugby and can be implemented across other sports such as field hockey.
        * Implement additional rest breaks that are not normally scheduled to occur. For example,
        3 to 5-min “quarter-time” breaks can be introduced mid-way through each half of a
        football or rugby match, or an extended 10-min drinks break can be introduced every
        hour of a cricket match or after the second set of a tennis match.
        * For sports with continuous play without any scheduled breaks, courses or play duration
        can be shortened
        * During all breaks in play or practice, everyone should seek shade – if natural shade is not
        available, portable sun shelters should be provided, and water freely available
            """,
    },
    "high": {
        "description": (
            "active cooling strategies should be applied during scheduled and"
            " additional rest breaks, or before and during activity if play is"
            " continuous. Below are strategies that have been shown to effectively"
            " reduce body temperature. The suitability and feasibility of each strategy"
            " will depend on the type of sport or exercise you are performing. "
        ),
        "suggestions": """
        * Drinking cold fluids and/or ice slushies before exercise commences. Note that cold water
        and ice slushy ingestion during exercise is less effective for cooling.
        * Submerging your arms/feet in cold water.
        * Water dousing – wetting your skin with cool water using a sponge or a spray bottle helps
        increase evaporation, which is the most effective cooling mechanism in the heat.
        * Ice packs/towels – placing an ice pack or damp towel filled with crushed ice around your
        neck.
        * Electric (misting) fans – outdoor fans can help keep your body cool, especially when
        combined with a water misting system.
            """,
    },
    "extreme": {
        "description": (
            "exercise/play should be suspended. If play has commenced, then all"
            " activities should be stopped as soon as possible."
        ),
        "suggestions": """
        * All players should seek shade or cool refuge in an air-conditioned space if available
        * Active cooling strategies should be applied.
            """,
    },
}


def get_yr_weather(lat=-33.8862, lon=151.1791):
    """get weather forecast from YR website"""

    weather = requests.get(
        f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}",
        headers={
            "User-Agent": "https://federicotartarini.github.io/air-quality-weather-sg"
        },
    )

    df_weather = pd.json_normalize(
        weather.json()["properties"]["timeseries"],
    )
    df_weather = df_weather[df_weather.columns[:7]]
    df_weather.columns = ["time", "pressure", "tdb", "cloud", "rh", "w-dir", "wind"]
    df_weather.set_index(pd.to_datetime(df_weather["time"]), inplace=True)
    df_weather.drop(columns=["time"], inplace=True)
    df_weather.index = df_weather.index.tz_convert(pytz.timezone("Australia/Sydney"))
    df_weather = df_weather.resample("2H").max()

    return df_weather


def calculate_comfort_indices(data):

    data["moderate"] = 0.1589 * data["tdb"] ** 2 - 15.494 * data["tdb"] + 362.71
    data["high"] = 0.1353 * data["tdb"] ** 2 - 14.312 * data["tdb"] + 363.2
    data["extreme"] = 360.36 - 13.016 * data["tdb"] + 0.1116 * data["tdb"] ** 2

    data["risk"] = "low"
    for risk in ["moderate", "high", "extreme"]:
        data.loc[data[risk] < 0, risk] = 0
        data.loc[data[risk] > 100, risk] = 100
        data.loc[(data["tdb"] > 26) & (data["rh"] > data[risk]), "risk"] = risk

    risk_value = {"low": 0, "moderate": 1, "high": 2, "extreme": 3}
    data["risk_value"] = data["risk"].map(risk_value)

    return data


if __name__ == "__main__":
    df = get_yr_weather(lat=-33.889, lon=151.184)
    df_results = calculate_comfort_indices(df)

    # test
    values = []
    for t in np.arange(10, 50):
        for rh in np.arange(0, 100, 1):
            values.append([t, rh])
    df = pd.DataFrame(values, columns=["tdb", "rh"])
    df_results = calculate_comfort_indices(data=df)
    df_plot = df_results.pivot("rh", "tdb", "risk").sort_index(ascending=False)
