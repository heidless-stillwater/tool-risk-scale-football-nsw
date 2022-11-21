import dash_bootstrap_components as dbc


def my_navbar():
    return dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("About", href="about")),
            # dbc.NavItem(dbc.NavLink("Settings", href="settings")),
        ],
        brand="SMA Extreme Heat Policy",
        brand_href="/",
        color="#E64626",
        dark=True,
    )
