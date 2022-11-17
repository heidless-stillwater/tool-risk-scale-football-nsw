import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)

import pandas as pd
import matplotlib.pyplot as plt
import requests
from pythermalcomfort.models import phs, set_tmp, utci, solar_gain, pet_steady
from pvlib import location
import pytz

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
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

    return df_weather


# def get_bom_data():
#
#     r = requests.get(
#         "http://www.bom.gov.au/places/nsw/camperdown/forecast/detailed/",
#         headers=headers,
#     )
#
#     soup = BeautifulSoup(r.content, "html.parser")
#
#     date_info = soup.find_all("div", class_="forecast-day collapsible")
#     dates = []
#     for date in date_info:
#         # print(date.attrs['id'].lstrip('d'))
#         dates.append(date.attrs["id"].lstrip("d"))
#
#     # soup.find_all("th", text="From")[0].parent.find_all("th")[1].text
#     times = pd.date_range(
#         start=f"{dates[0]} 02:00:00", end=f"{dates[-1]} 23:00:00", freq="3H"
#     )
#
#     values = {
#         "tdb": "Air temperature (°C)",
#         "rh": "Relative humidity (%)",
#         "rain_chance": "Chance of any rain",
#         "dew": "Dew point temperature (°C)",
#         "feel": "Feels like (°C)",
#         "UV": "UV Index",
#         "wind": "Wind speed",
#     }
#     results = {
#         "tdb": [],
#         "rh": [],
#         "rain_chance": [],
#         "dew": [],
#         "feel": [],
#         "UV": [],
#         "wind": [],
#         "timestamp": times,
#     }
#     for value in values:
#         tds = soup.find_all("th")
#         for td in tds:
#             if values[value] not in td.text:
#                 continue
#             numbers = td.parent.find_all("td")
#             for el in numbers:
#                 if value == "wind":
#                     try:
#                         results[value].append(
#                             int(str(el).split('data-kmh="')[1].split('"')[0]) / 3.6
#                         )
#                     except IndexError:
#                         results[value].append(float("nan"))
#
#                 else:
#                     try:
#                         results[value].append(int(str(el.text).replace("%", "")))
#                     except ValueError:
#                         results[value].append(float("nan"))
#
#     return (
#         pd.DataFrame.from_records(results).dropna(subset=["tdb"]).set_index("timestamp")
#     )


def calculate_comfort_indices(location_user=[-33.889, 151.184]):

    wind_coefficient = 0.3
    lat, lon = location_user

    df_for = get_yr_weather(lat, lon)

    tz = pytz.timezone("Australia/Sydney")
    site_location = location.Location(lat, lon, tz=tz, name="Sydney, AU")
    solar_position = site_location.get_solarposition(df_for.index)
    cs = site_location.get_clearsky(df_for.index)

    # correct solar radiation by cloud cover
    solar_position.loc[solar_position["elevation"] < 0, "elevation"] = 0
    sharp = 0
    sol_transmittance = 1
    f_svv = 1
    f_bes = 1
    asw = 0.7
    posture = "standing"
    floor_reflectance = 0.1

    df_for = pd.concat([df_for, solar_position], axis=1)
    df_for = pd.concat([df_for, cs], axis=1)

    df_for["cloud"] /= 10
    df_for["dni"] *= (
        -0.00375838 * df_for["cloud"] ** 2 + -0.06230424 * df_for["cloud"] + 1.02290071
    )

    results = []
    for ix, row in df_for.iterrows():
        erf_mrt = solar_gain(
            row["elevation"],
            sharp,
            row["dni"],
            sol_transmittance,
            f_svv,
            f_bes,
            asw,
            posture,
            floor_reflectance,
        )
        if erf_mrt["delta_mrt"] < 0:
            print(row)
        results.append(erf_mrt)
    df_mrt = pd.DataFrame.from_dict(results)
    df_mrt.set_index(df_for.index, inplace=True)
    df_for = pd.concat([df_for, df_mrt], axis=1)

    df_for["wind"] *= wind_coefficient
    df_for["tr"] = df_for["tdb"] + df_for["delta_mrt"]
    df_for["clo"] = (
        1.372
        - 0.01866 * df_for["tdb"]
        - 0.0004849 * df_for["tdb"] ** 2
        - 0.000009333 * df_for["tdb"] ** 3
    )
    df_for["clo"] = 0.3

    df_for["utci"] = utci(
        tdb=df_for["tdb"], tr=df_for["tr"], v=df_for["wind"], rh=df_for["rh"]
    )
    df_for["set"] = set_tmp(
        tdb=df_for["tdb"],
        tr=df_for["tr"],
        v=df_for["wind"],
        rh=df_for["rh"],
        met=1.1,
        clo=df_for["clo"],
        limit_inputs=False,
    )

    df_for = df_for.resample("1H").interpolate("linear")

    map_index = {
        "set": {
            "cool": 17,
            "comfortable": 30,
            "warm": 34,
            "hot": 37,
            "very hot": 999,
        },
    }

    for index in map_index:
        scale = map_index[index]
        df_for[f"hss_{index}"] = pd.cut(
            df_for[index],
            bins=[-99] + list(scale.values()),
            labels=list(scale.keys()),
        )

    map_hss = {
        "very cold": 1,
        "cold": 1,
        "cool": 1,
        "comfortable": 2,
        "warm": 3,
        "hot": 4,
        "very hot": 5,
    }

    df_for["hss"] = df_for["hss_set"].map(map_hss)

    return df_for


if __name__ == "__main__":
    df = calculate_comfort_indices()
    df.loc[df["hss"] > 2, ["tdb", "tr", "rh", "clo", "wind", "set"]].round(1)
    df.loc[df["tr"] > 60, ["tdb", "tr", "rh", "clo", "wind", "set"]].round(1)
    df[["set", "tdb", "tr"]].plot()
    plt.show()
