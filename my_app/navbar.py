import dash_bootstrap_components as dbc
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from dash_bootstrap_components._components.Container import Container


# def my_navbar():
#     return dbc.NavbarSimple(
#         children=[
#             dbc.NavItem(dbc.NavLink("Home", href="/")),
#             dbc.NavItem(dbc.NavLink("About", href="/about")),
#             dbc.NavItem(dbc.NavLink("Settings", href="/settings")),
#         ],
#         brand="SMA Extreme Heat Policy",
#         brand_href="/",
#         color="#E64626",
#         dark=True,
#     )


PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"


def my_navbar():
    return dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                            dbc.Col(dbc.NavbarBrand("Logo", className="ms-2")),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="/",
                    style={"textDecoration": "none"},
                ),
                dbc.NavbarToggler(id="navbar-toggle", n_clicks=0),
                dbc.Collapse(
                    dbc.Nav(
                        [
                            dbc.NavItem(dbc.NavLink("Home", href="/")),
                            dbc.NavItem(dbc.NavLink("About", href="/about")),
                            dbc.NavItem(dbc.NavLink("Settings", href="/settings")),
                        ],
                        className="ms-auto",
                        navbar=True,
                    ),
                    id="navbar-collapse",
                    navbar=True,
                ),
            ],
        ),
        color="dark",
        dark=True,
        className="mb-5",
    )
