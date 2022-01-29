import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
import plotly.io as pio
import json
import platform

def hood_map():

    file_path = str()

    # check platform to get file location for geojson
    if platform.platform() == 'Linux-5.10.60.1-microsoft-standard-WSL2-x86_64-with-glibc2.29':
        file_path = "/home/jliu/project/todata/views/explore/hoods/neighbourhoods.geojson"
    else:
        file_path = "/home/project/todata/views/explore/hoods/neighbourhoods.geojson"

    # import data files
    hood = gpd.read_file(file_path)
    stats = pd.read_csv("./todata/data/files/census/hood_data.csv")

    # clean and join data
    hood = hood[['AREA_SHORT_CODE','geometry']]
    merged = pd.merge(hood, stats, how='left', left_on='AREA_SHORT_CODE', right_on='number').drop('AREA_SHORT_CODE', axis=1)
    merged.set_index('name', inplace=True)
    geometry = json.loads(merged.geometry.to_json())
    merged_trim = merged.drop(['geometry', 'number'], axis=1)

    # generate choropleth map
    fig = go.Figure(go.Choroplethmapbox(geojson=geometry, 
                                    locations=merged.index,
                                    featureidkey="id",
                                    z=merged['Population density per sq km'],
                                    marker_opacity=0.75,
                                    marker_line_width=0.5,
                                    hoverinfo = 'z+location',
                                    hoverlabel = dict(namelength=-1)
                                    )
                )
                

    fig.update_layout(coloraxis_colorscale='Viridis',
                    mapbox=dict(style='carto-positron',
                                zoom=9.5, 
                                center = {'lat': 43.7232, 'lon':-79.3832},
                                )) 

    def create_layout_button(column):
        return dict(label = column,
                    method = 'update',
                    args = [{'z': [merged_trim[column]],
                            }])

    fig.update_layout(
        updatemenus=[go.layout.Updatemenu(
            active = 0,
            buttons = list(merged_trim.columns.map(lambda column: create_layout_button(column))),
            direction="down",
            showactive=True,
            x=0,
            xanchor="left",
            y=1,
            yanchor="top",
            )
        ],
    )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    plot = pio.to_html(fig, full_html=False, config={"displayModeBar": False})

    return plot