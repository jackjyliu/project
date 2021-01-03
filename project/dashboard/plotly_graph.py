"""
plotly module to test insert into flask views
"""

import plotly.express as px
import plotly.io 
from project.models.credentials import WSL2_PSQL as psql
from project.models.sql_load import sql_read

def plotly_test():
    power_df = sql_read('toronto',
                        """
                        SELECT  ts,
                                power_use_mwh,
                                EXTRACT(YEAR FROM ts) AS year,
                                EXTRACT(MONTH FROM ts) AS month,
                                EXTRACT(ISODOW FROM ts ) AS day_of_week,
                                EXTRACT(HOUR FROM ts) as hour
                        FROM power
                        WHERE power_use_mwh > 1
                        """
                        )

    fig = px.density_heatmap(power_df, x='hour', y='month', z='power_use_mwh', histfunc='avg')
    html_plot = plotly.io.to_html(fig, full_html=False)

    return html_plot
