"""
plotly module to test insert into flask views
"""

import plotly.express as px
import plotly.io as pio
from todata.models.sql.functions import sql_read_pd
import pandas as pd


def day_hour_heatmap():

    pio.templates.default = "simple_white"

    df = sql_read_pd(
        "toronto",
        """
                        SELECT  ts,
                                power_use_mwh,
                                --EXTRACT(YEAR FROM ts) AS year,
                                --EXTRACT(MONTH FROM ts) AS month,
                                EXTRACT(ISODOW FROM ts ) AS day_of_week,
                                EXTRACT(HOUR FROM ts) as hour
                        FROM power
                        WHERE power_use_mwh > 1
                        """,
    )

    fig = px.density_heatmap(
        df, x="hour", y="day_of_week", z="power_use_mwh", histfunc="avg"
    )
    fig.update_layout(
        title="Average Usage by Hour and Day of Week",
        title_x=0.5,
        xaxis_title="Hour",
        yaxis_title="Day (1=Monday)",
        coloraxis_colorbar={"title": "MegawattHour"},
        yaxis={"autorange": "reversed"},
        plot_bgcolor="white",
    )
    fig.add_annotation(
        text="Source: IESO",
        xref="paper",
        x=1,
        yref="paper",
        y=-0.15,
        showarrow=False,
        font={"color": "#A9A9A9"},
    )

    plot = pio.to_html(fig, full_html=False)

    return plot


def daily_power_usage():

    pio.templates.default = "simple_white"

    df = sql_read_pd(
        "toronto",
        """
                        WITH daily_use AS(
                        SELECT  DATE_TRUNC('day', ts) AS date, 
                                SUM(power_use_mwh) AS power_use_mwh
                        FROM power
                        WHERE power_use_mwh > 10
                        GROUP BY date
                        ORDER BY date)

                        SELECT  date,
                                power_use_mwh,
                                ROUND(AVG(power_use_mwh)
                                OVER(ORDER BY date ASC ROWS BETWEEN 30 PRECEDING AND CURRENT ROW),0)
                                AS moving_avg
                        FROM daily_use
                        ORDER BY date
                        """,
    )

    fig = px.line(df, x="date", y=["power_use_mwh", "moving_avg"])
    fig.update_traces(hovertemplate=None)
    fig.update_layout(
        title="Daily Usage",
        xaxis_title="Date",
        yaxis_title="MegawattHour",
        legend_title=None,
        title_x=0.5,
        showlegend=True,
        plot_bgcolor="white",
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
            type="date",
        )
    )

    plot = pio.to_html(fig, full_html=False)

    return plot


def seasonal_power_usage():

    pio.templates.default = "simple_white"

    df = sql_read_pd(
        "toronto",
        """
                        SELECT  ROUND(AVG(power_use_mwh)) AS avg_power_usage,
                                EXTRACT(MONTH FROM ts) AS month,
                                EXTRACT(HOUR FROM ts) as hour
                        FROM power
                        WHERE power_use_mwh > 1
                        GROUP BY month, hour
                        ORDER BY month, hour                        
                        """,
    )

    # group hourly use into 4 seasons
    season_map = {
        1: "Dec-Feb",
        2: "Dec-Feb",
        3: "Mar-May",
        4: "Mar-May",
        5: "Mar-May",
        6: "Jun-Aug",
        7: "Jun-Aug",
        8: "Jun-Aug",
        9: "Sep-Nov",
        10: "Sep-Nov",
        11: "Sep-Nov",
        12: "Dec-Feb",
    }

    df["season"] = df["month"].map(season_map)
    df.drop(columns=["month"], inplace=True)
    df = df.groupby(["season", "hour"]).mean().reset_index()
    df["avg_power_usage"] = df["avg_power_usage"].round(0)
    pvt = df.pivot(
        index="hour", columns="season", values="avg_power_usage"
    ).reset_index()

    # plot into 4 line graphs
    fig = px.line(pvt, x="hour", y=["Dec-Feb", "Mar-May", "Jun-Aug", "Sep-Nov"])
    fig.update_traces(hovertemplate=None)
    fig.update_layout(
        title="Seasonal Usage Pattern",
        title_x=0.5,
        xaxis_title="Hour",
        yaxis_title="MegawattHour",
        legend_title="Months",
        showlegend=True,
        plot_bgcolor="white",
        hovermode="x unified",
    )

    plot = pio.to_html(fig, full_html=False)

    return plot