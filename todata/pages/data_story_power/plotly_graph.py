"""
plotly module to test insert into flask views
"""

import plotly.express as px
import plotly.io 
from todata.models.credentials import WSL2_PSQL as psql
from todata.models.sql_load import sql_read

def month_hour_heatmap():
    df = sql_read('toronto',
                        """
                        SELECT  ts,
                                power_use_mwh,
                                --EXTRACT(YEAR FROM ts) AS year,
                                --EXTRACT(MONTH FROM ts) AS month,
                                EXTRACT(ISODOW FROM ts ) AS day_of_week,
                                EXTRACT(HOUR FROM ts) as hour
                        FROM power
                        WHERE power_use_mwh > 1
                        """
                        )

    fig = px.density_heatmap(df, x='hour', y='day_of_week', z='power_use_mwh', histfunc='avg')
    fig.update_layout(
            title='Average Usage by Hour and Day of Week',
            title_x=0.5,
            coloraxis_colorbar={'title': 'MegawattHour'},
            yaxis={'autorange':'reversed'},
            plot_bgcolor="white"
            )
    plot = plotly.io.to_html(fig, full_html=False)

    return plot

def monthly_power_use():
    df = sql_read('toronto',
                        """
                        SELECT  DATE_TRUNC('month', ts) AS month, 
                                SUM(power_use_mwh) AS power_use_mwh
                        FROM power
                        WHERE power_use_mwh > 1
                        GROUP BY Month
                        ORDER BY Month
                        """
                        )

    fig = px.line(df, x='month', y='power_use_mwh')
    fig.update_layout(
            title='Monthly Usage',
            title_x=0.5,
            showlegend=False,
            plot_bgcolor="white"
            )
    plot = plotly.io.to_html(fig, full_html=False)

    return plot