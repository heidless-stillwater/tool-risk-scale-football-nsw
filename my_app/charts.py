import plotly.express as px
import plotly.graph_objects as go

# from the AU museum https://australian.museum/about/organisation/media-centre/brand/colour/#Download
hss_palette = {
    1: "#006EB6",
    2: "#00AD7C",
    3: "#FFD039",
    4: "#E45A01",
    5: "#CB3327",
}


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
        margin=dict(
            autoexpand=True,
            l=0,
            r=20,
            t=0,
        ),
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


if __name__ == "__main__":
    pass
