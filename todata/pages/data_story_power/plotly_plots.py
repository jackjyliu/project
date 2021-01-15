"""
plotly module to test insert into flask views
"""

import plotly.express as px
import plotly.io 
from todata.models.credentials import WSL2_PSQL as psql
from todata.models.sql_functions import sql_read_pd


def month_hour_heatmap():
    df = sql_read_pd('toronto',
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
    fig.add_annotation(text="Source: IESO",
                        xref='paper', x=1,
                        yref='paper', y=-0.15,
                        showarrow=False,
                        font={'color':'#A9A9A9'}
                        )

    plot = plotly.io.to_html(fig, full_html=False)

    return plot

def monthly_power_use():
    df = sql_read_pd('toronto',
                        """
                        WITH monthly_use AS(
                        SELECT  DATE_TRUNC('month', ts) AS date, 
                                SUM(power_use_mwh) AS power_use_mwh
                        FROM power
                        WHERE power_use_mwh > 1 AND DATE_TRUNC('month', ts) < DATE_TRUNC('month', CURRENT_DATE)
                        GROUP BY date
                        ORDER BY date)

                        SELECT  date,
                                power_use_mwh,
                                ROUND(AVG(power_use_mwh)
                                OVER(ORDER BY date ASC ROWS BETWEEN 11 PRECEDING AND CURRENT ROW),0)
                                AS moving_avg_12m
                        FROM monthly_use
                        ORDER BY date
                        """
                        )

    fig = px.line(df, x='date', y=['power_use_mwh', 'moving_avg_12m'])
    fig.update_layout(
            title='Monthly Usage',
            title_x=0.5,
            showlegend=False,
            plot_bgcolor="white"
            )

    fig.add_annotation(text="Source: IESO",
                        xref='paper', x=1,
                        yref='paper', y=-0.15,
                        showarrow=False,
                        font={'color':'#A9A9A9'}
                        )
    plot = plotly.io.to_html(fig, full_html=False)

    return plot