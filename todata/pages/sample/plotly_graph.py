"""
plotly module to test insert into flask views
"""

import plotly.express as px
import plotly.io 
from todata.models.credentials import WSL2_PSQL as psql
from todata.models.sql_load import sql_read

def month_hour_heatmap():
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
    fig.update_layout(
            title='Toronto Power Use',
            title_x=0.5,
            legend_title_text='MegawattHour'
            )
    plot = plotly.io.to_html(fig, full_html=False)

    return plot
