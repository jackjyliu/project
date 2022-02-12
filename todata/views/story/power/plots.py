"""
plotly visuals for toronto power data
"""
import pandas as pd

import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import todata.views.plotly_custom_theme

from todata.data.sql.functions import sql_read_pd


pio.templates.default = "simple_white+custom"

def temperature_scatter():

    df = sql_read_pd(
        "toronto",
        """
        SELECT p.power_use_mwh, t.temp_c
        FROM power_demand p TABLESAMPLE BERNOULLI(10)
        LEFT JOIN weather_temperature t ON p.ts = t.ts
        WHERE power_use_mwh > 1 AND t.temp_c IS NOT NULL AND p.ts > '2018-01-01'
        """
    )

    fig = px.scatter(
        df,
        x="temp_c",
        y="power_use_mwh",
        opacity=0.2,
        trendline="lowess",
        trendline_options=dict(frac=0.35),
        trendline_color_override="#555555"
    )

    fig.update_layout(
        title="Power vs Temperature",
        title_x=0.5,
        xaxis_title="Temperature C",
        yaxis_title="MegaWattHour",
        margin={"r": 0, "l": 0, "b": 0}
    )

    fig.update_traces(hovertemplate="Temperature %{x}c<br>%{y} MWh")
    
    plot = pio.to_html(fig, full_html=False, config={"displayModeBar": False})

    return plot


def day_hour_heatmap():

    df = sql_read_pd(
        "toronto",
        """
        SELECT  --ts,
                power_use_mwh,
                --EXTRACT(YEAR FROM ts) AS year,
                --EXTRACT(MONTH FROM ts) AS month,
                EXTRACT(ISODOW FROM ts ) AS day_of_week,
                EXTRACT(HOUR FROM ts) as hour
        FROM power_demand
        WHERE power_use_mwh > 1 AND ts > '2010-01-01'
        """
    )

    fig = px.density_heatmap(
        df, x="hour", y="day_of_week", z="power_use_mwh", histfunc="avg", color_continuous_scale=px.colors.sequential.Blues
    )
    fig.update_layout(
        title="Average Usage by Hour and Day of Week",
        title_x=0.5,
        xaxis_title="Hour",
        yaxis_title="Day (1=Monday)",
        coloraxis_colorbar={"title": "MegaWattHour"},
        yaxis={"autorange": "reversed"},
        plot_bgcolor="white",
        margin={"r": 0, "l": 0, "b": 0},
    )
    fig.update_traces(hovertemplate="%{x}:00<br>Day %{y}<br>%{z} MWh")

    """
    fig.add_annotation(
        text="Source: IESO",
        xref="paper",
        x=1,
        yref="paper",
        y=-0.15,
        showarrow=False,
        font={"color": "#A9A9A9"}
    )
    """
    plot = pio.to_html(fig, full_html=False, config={"displayModeBar": False})

    return plot


def daily_power_usage():

    df = sql_read_pd(
        "toronto",
        """
                        WITH daily_use AS(
                        SELECT  DATE_TRUNC('day', ts) AS date, 
                                SUM(power_use_mwh) AS power_use_mwh
                        FROM power_demand
                        WHERE power_use_mwh > 100 AND ts > '2010-01-01'
                        GROUP BY date
                        ORDER BY date)

                        SELECT  date,
                                power_use_mwh,
                                ROUND(AVG(power_use_mwh)
                                OVER(ORDER BY date ASC ROWS BETWEEN 30 PRECEDING AND 30 FOLLOWING),0)
                                AS smoothed_avg
                        FROM daily_use
                        ORDER BY date
                        """
    )

    fig = px.line(df, x="date", y=["power_use_mwh", "smoothed_avg"])
    fig.update_traces(hovertemplate=None)
    fig.update_layout(
        title="Daily Usage",
        xaxis_title="Date",
        yaxis_title="MegaWattHour",
        legend_title=None,
        title_x=0.5,
        showlegend=True,
        plot_bgcolor="white",
        legend=dict(x=0.05, y=1),
        margin={"r": 15, "l": 0, "b": 0}
    )

    # Add range slider
    
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
            rangeslider=dict(visible=True),
            type="date"
        )
    )

    plot = pio.to_html(fig, full_html=False, config={"displayModeBar": False})

    return plot


def temp_effect():
    file_path = './todata/static/stories/power/power_predictions.csv'

    temp = pd.read_csv(file_path)

    fig = px.line(temp, x='day', y='power_mwh', color='temperature', range_y=[100000,200000],
                color_discrete_map={
                    'actual':'#2171b5',
                    'temp +1c':'#f9d5e5',
                    'temp +2c':'#eeac99',
                    'temp +3c':'#e06377'
                })
    
    fig.update_traces(hovertemplate=None)
    fig.update_layout(
        title="Simulated 2021 Power Usage",
        title_x=0.5,
        xaxis_title="date",
        yaxis_title="MegaWattHour",
        legend=dict(x=0.05, y=1),
        margin={"r": 0, "l": 0, "b": 0},
        hovermode  = 'x unified',
        xaxis=dict(
            rangeslider=dict(visible=True),
            type="date"
        )
    )

    plot = pio.to_html(fig, full_html=False, config={"displayModeBar": False})

    return plot