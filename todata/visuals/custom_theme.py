"""
default plotly template for visuals
"""

import plotly.graph_objects as go
import plotly.io as pio

pio.templates['custom'] = go.layout.Template(
    layout=dict(
        font=dict(color='#808080', family='Helvetica'),
        colorway=['#1F77B4','#185a88','#1b699e','#1f77b4','#2385ca','#2b93db','#419ede']
        )
)