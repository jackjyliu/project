"""
default plotly template for visuals
"""

import plotly.graph_objects as go
import plotly.io as pio

pio.templates['custom'] = go.layout.Template(
    layout=dict(
        font=dict(color='#696969', family='Helvetica')
        )
)