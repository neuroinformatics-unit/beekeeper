"""Metadata page layout for the beekeeping application.

This module defines the layout for the metadata page where users
can view and manage video metadata.
"""

import dash
from dash import html

######################
# Add page to registry
#########################
dash.register_page(__name__)


###############
# Layout
################
# Metadata layout
layout = html.Div(
    children=[
        html.H1(children="Metadata"),
        html.Div(
            id="metadata-container", style={"height": "1200px"}, children=[]
        ),  # component to hold the output from the data upload
    ]
)
