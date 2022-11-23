import plotly.express as px
import numpy as np
import pandas as pd
from utils import calculate_comfort_indices, hss_palette
import plotly.graph_objects as go


def standard_layout(fig):

    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor="rgb(204, 204, 204)",
            linewidth=2,
            ticks="outside",
            tickfont=dict(
                family="Arial",
                size=12,
                color="rgb(82, 82, 82)",
            ),
            title_text="",
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            showline=False,
            showticklabels=True,
        ),
        autosize=True,
        margin=dict(autoexpand=True, l=0, r=0, t=0, b=0),
        showlegend=False,
        plot_bgcolor="white",
    )

    return fig


def line_chart_tmp(df):
    fig = px.line(
        df,
        x=df.index,
        y="tdb",
        height=200,
    )

    return standard_layout(fig)


def heatmap_chart_tmp(df):
    fig = px.imshow(
        [list(df["hss"].values)],
        color_continuous_scale=list(hss_palette.values()),
        height=200,
        aspect="auto",
        range_color=[0, 5],
    )
    fig = standard_layout(fig)
    fig.update_layout(coloraxis_showscale=False)
    # fig.update_xaxes(
    #     tickslabels=[f"{x[0]}-{x[1]}" for x in zip(df.index.day, df.index.hour)]
    # )
    fig.update_yaxes(showticklabels=False, tickvals=[""])

    return standard_layout(fig)


def hss_trend(df):
    fig = px.bar(
        df,
        x=df.index,
        y="hss",
        color=list(df["hss"]),
        height=200,
        color_continuous_scale=list(hss_palette.values()),
        range_color=[0, 5],
    )
    fig.update(layout_coloraxis_showscale=False)
    fig.update_yaxes(title_text="")

    return standard_layout(fig)


def hss_gauge(df):
    # https://plotly.com/python/gauge-charts/
    fig = go.Figure(
        go.Indicator(
            domain={"x": [0, 1], "y": [0, 1]},
            value=df["hss"][0],
            mode="gauge+number",
            gauge={
                "axis": {"range": [0, 5]},
                "steps": [
                    {"range": [x - 1, x], "color": hss_palette[x]} for x in hss_palette
                ],
                "borderwidth": 1,
                "bar": {"color": "#000", "line": {"width": 0}},
                "threshold": {
                    "line": {"color": "black", "width": 20},
                    "thickness": 0.75,
                    "value": df["hss"][0],
                },
            },
        )
    )

    return standard_layout(fig)


def indicator_chart(df_for, sport_class):

    df = calculate_comfort_indices(data_for=df_for, sport_class=sport_class)
    data = df.iloc[0]
    steps = [
        {"range": [0, data["moderate"]], "color": hss_palette[0]},
        {"range": [data["moderate"], data["high"]], "color": hss_palette[1]},
        {"range": [data["high"], data["extreme"]], "color": hss_palette[2]},
        {"range": [data["extreme"], 100], "color": hss_palette[3]},
    ]

    fig = go.Figure(
        go.Indicator(
            mode="gauge",
            value=data["rh"],
            domain={"x": [0, 1], "y": [0, 1]},
            gauge={
                "shape": "bullet",
                "axis": {"range": [0, 100]},
                "steps": steps,
                "bar": {"color": "black"},
            },
        )
    )
    fig.add_annotation(
        x=data["rh"] / 100, y=1, text="Now", showarrow=False, font=dict(color="#000")
    )
    fig = standard_layout(fig)
    fig.update_layout(height=60)
    return fig


def risk_map(df_for, sport_class):

    values = []
    t_min, t_max = 23, 45
    for t in np.arange(t_min, t_max + 1):
        for rh in np.arange(0, 100):
            values.append([t, rh])
    df = pd.DataFrame(values, columns=["tdb", "rh"])
    df = calculate_comfort_indices(data_for=df, sport_class=sport_class)
    df["top"] = 100

    df_for = df_for.head(10)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["tdb"],
            y=df["moderate"],
            fill="tozeroy",
            fillcolor=hss_palette[0],
            mode="none",
        )
    )
    for ix, risk in enumerate(["high", "extreme", "top"]):
        fig.add_trace(
            go.Scatter(
                x=df["tdb"],
                y=df[risk],
                fill="tonexty",
                fillcolor=hss_palette[ix + 1],
                mode="none",
            )
        )
    fig.add_trace(
        go.Scatter(
            x=df_for["tdb"],
            y=df_for["rh"],
            mode="lines+markers+text",
            line_color="black",
            text=df_for.index.hour,
            textposition="top center",
            line={"shape": "spline", "smoothing": 1.3},
        )
    )

    fig = standard_layout(fig)
    fig.update_layout(
        xaxis=dict(title_text="Temperature [°C]", range=[t_min, t_max], dtick=2),
        yaxis=dict(title_text="Relative Humidity [%]", range=[5, 95]),
    )
    return fig
