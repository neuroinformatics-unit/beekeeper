"""Main Dash application module for beekeeping.

This module contains the main Dash application initialization, layout
definition, and callback registration for the beekeeping web application.
"""

import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html

import beekeeping.callbacks.home as home
import beekeeping.callbacks.metadata as metadata

#################
# Initialise app
#################
app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    # TODO: is there an alternative to prevent error w/ chained callbacks?
)

###############
# Components
###############
# Sidebar style
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# Sidebar component
sidebar = html.Div(
    [
        html.H2("beekeeping 🐝", className="display-4"),
        html.Hr(),
        html.P(
            [
                "Managing",
                html.Br(),
                "video metadata",
                html.Br(),
                "for animal behaviour",
                html.Br(),
                "experiments",
            ],
            className="lead",
        ),
        dbc.Nav(
            children=[
                dcc.Link(
                    id="link-" + page["name"].replace(" ", "-"),
                    children=f"{page['name']}",
                    href=page["relative_path"],  # url of each page
                )
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
    id="sidebar",
)

# Main content style
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# Main content component
content = html.Div(
    id="page-content",
    children=dash.page_container,
    style=CONTENT_STYLE,
)

# Storage component for the session
storage = dcc.Store(
    id="session-storage",
    storage_type="session",
    data=tuple(),
)

###############
# Layout
################
app.layout = html.Div(
    [
        dcc.Location(id="url"),
        sidebar,
        content,
        storage,
    ]
)


###############
# Callbacks
################
home.get_callbacks(app)
metadata.get_callbacks(app)


def startbeekeeping():
    """Start the beekeeping Dash application server."""
    app.run(debug=True)


###############
# Driver
################
if __name__ == "__main__":
    startbeekeeping()
