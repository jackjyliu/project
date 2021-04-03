from todata.data.sql.functions import sql_read_pd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import todata.views.plotly_custom_theme
pio.templates.default = "simple_white+custom"


def multi_plot(df, addAll=True):
    """
    generates plotly multiple line plot html code from pandas dataframe 
    """

    fig = go.Figure()
    
    # create multiple line plot
    for column in df.columns.to_list():
        fig.add_trace(
            go.Scatter(
                x = df.index,
                y = df[column],
                name = column
            )
        )

    button_all = dict(label = 'All',
                      method = 'update',
                      args = [{'visible': df.columns.isin(df.columns),
                               'title': 'All',
                               'showlegend':False}])

    def create_layout_button(column):
        return dict(label = column,
                    method = 'update',
                    args = [{'visible': df.columns.isin([column]),
                            'title': column,
                            'showlegend': False}])

    fig.update_layout(
        updatemenus=[go.layout.Updatemenu(
            active = 0,
            buttons = ([button_all] * addAll) + list(df.columns.map(lambda column: create_layout_button(column))),
            direction="down",
            showactive=True,
            x=0,
            xanchor="left",
            y=1,
            yanchor="top",
            )
        ],
    )
    
    # add slider
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(visible=True),
            type="date"
        ),
        margin={"r": 5, "l": 0, "b": 0, "t":20},
    )

    # convert to html code
    plot = pio.to_html(fig, full_html=False, config={"displayModeBar": False})
    
    return plot


def line_plot():
    """
    plotly line plot of monthly toronto indicators
    """

    ts = sql_read_pd("toronto",
        """
        WITH bus AS (
            SELECT date_trunc('month', issued_date) as datem, COUNT(issued_date) AS licence_issued
            FROM business_licence
            GROUP BY date_trunc('month', issued_date)
        ),
        dev AS (
            SELECT date_trunc('month', date_submit) as datem, COUNT(date_submit) AS dev_applications
            FROM development_application
            GROUP BY date_trunc('month', date_submit)
        ),
        power AS (
            SELECT date_trunc('month', ts) as ts, SUM(power_use_mwh) AS power_mwh
            FROM power_demand
            GROUP BY date_trunc('month', ts)
        ),
        water AS (
            SELECT date_trunc('month', ts) as ts, SUM(water_megalitre) AS water_megalitre
            FROM water_use
            GROUP BY date_trunc('month', ts)
        )

        SELECT 
            tm
            , ei.persons as ei_persons
            , fl.flights as yyz_flights
            , gs.cents as gas_cents
            , hs.units as house_start_units
            , hc.units as house_comp_units
            , mf.sales as manufacture_dollars
            , rt.sales as retail_dollars
            , bus.licence_issued as licence_issued
            , dev.dev_applications
            , p.power_mwh
            , w.water_megalitre
            
        FROM 
            generate_series(timestamp '2000-01-01'
                            , CURRENT_TIMESTAMP - INTERVAL '1 month'
                            , interval '1 month'
                            ) AS tm

        LEFT JOIN statcan_ei ei ON tm = ei.series_date
        LEFT JOIN statcan_flights fl ON tm = fl.series_date
        LEFT JOIN statcan_gas_price gs ON tm = gs.series_date
        LEFT JOIN statcan_housing_starts hs ON tm = hs.series_date
        LEFT JOIN statcan_housing_completion hc ON tm = hc.series_date
        LEFT JOIN statcan_manufacture mf ON tm = mf.series_date
        LEFT JOIN statcan_retail rt ON tm = rt.series_date
        LEFT JOIN bus ON tm = bus.datem
        LEFT JOIN dev ON tm = dev.datem
        LEFT JOIN power p ON tm = p.ts
        LEFT JOIN water w ON tm = w.ts

        ORDER BY tm ASC
        """)

    ts_index = ts.set_index('tm')

    return multi_plot(ts_index)
