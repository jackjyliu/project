"""
collection of functions to pull toronto related data from public sources, cleaned, formatted and returned as pandas dataframe
"""

from datetime import datetime
import calendar
import pandas as pd
import requests
from io import BytesIO
from todata.data.utils.datetime import utc_to_local_time


def toronto_power(start_year=datetime.today().year, end_year=datetime.today().year):
    """
    enter years needed for as list, valid for years >= 2004

    returns zonal demand csv file from ieso ftp server as pandas dataframe
    DateTime in 1 hour blocks
    Power in MWh
    """
    if start_year < 2004 or end_year > datetime.today().year:
        raise Exception("Please check the year range")

    # list of pandas dataframes
    power_df_list = list()

    # load power data by year
    for year in range(start_year, end_year + 1):
        power_file = pd.read_csv(
            f"http://reports.ieso.ca/public/DemandZonal/PUB_DemandZonal_{year}.csv",
            skiprows=3,
        )
        power_file["DateTime"] = pd.to_datetime(
            power_file["Date"] + " " + power_file["Hour"].add(-1).astype(str) + ":00:00"
        )
        toronto_power = power_file[["DateTime", "Toronto"]].copy()
        toronto_power.columns = ["ts", "power_use_mwh"]

        power_df_list.append(toronto_power)

    # concat pandas dataframes
    toronto_power_df = pd.concat(power_df_list)

    return toronto_power_df


def toronto_daylight(
    start_year=datetime.today().year,
    end_year=datetime.today().year,
    path="todata/data/files/daylight/toronto_daylight.txt",
):
    """
    return pandas dataframe of toronto daylight hours
    please enter start_year and end_year
    """
    # load daylight file
    daylight_raw = pd.read_csv(path, skiprows=2, sep="\s+", header="infer")
    daylight_raw["combined_date"] = (
        daylight_raw.index.values + " " + daylight_raw["Date"].map(str)
    )

    # empty list for cleaned dataframes
    daylight_df_list = list()

    for year in range(start_year, end_year + 1):
        ys = str(year)
        daylight_temp = daylight_raw.copy()

        # delete Feb 29 from daylight temp df to avoid errors
        if not calendar.isleap(year):
            daylight_temp = daylight_temp[daylight_temp["combined_date"] != "Feb 29"]

        # covert to datetime format
        daylight_temp["date"] = pd.to_datetime(
            ys + " " + daylight_temp["combined_date"], format="%Y %b %d"
        )
        daylight_temp["rise"] = pd.to_datetime(
            ys + " " + daylight_temp["combined_date"] + " " + daylight_temp["Rise"],
            format="%Y %b %d %H:%M",
        )
        daylight_temp["set"] = pd.to_datetime(
            ys + " " + daylight_temp["combined_date"] + " " + daylight_temp["Set"],
            format="%Y %b %d %H:%M",
        )

        daylight_clean = daylight_temp[["date", "rise", "set", "Day"]].copy()
        daylight_clean.columns = ["date", "rise", "set", "hours"]
        daylight_clean.reset_index(inplace=True, drop=True)

        daylight_df_list.append(daylight_clean)

    toronto_daylight_df = pd.concat(daylight_df_list)

    return toronto_daylight_df


def toronto_temperature(
    start_year=datetime.today().year, end_year=datetime.today().year, station_id=31688
):
    """
    start_year and end_year
    returns Toronto City Centre weather station (default) as pandas dataframe
    toronto_weather(year>2002, month)
    """
    if start_year < 2002 or end_year > datetime.today().year:
        raise Exception("Please check the year range")

    # list of pandas dataframes
    weather_df_list = list()

    # get monthly weather
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            url = f"https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID={station_id}&Year={year}&Month={month}&Day=1&timeframe=1&submit= Download+Data"
            req = requests.get(url)
            weather_raw = BytesIO(req.content)

            weather = pd.read_csv(weather_raw)
            weather["DateTime"] = pd.to_datetime(weather["Date/Time (LST)"])
            weather = weather[
                ["DateTime", "Temp (°C)", "Rel Hum (%)", "Stn Press (kPa)", "Precip. Amount (mm)"]
            ]
            weather.columns = ["ts", "temp_c", "rel_hum_pct", "pressure_kpa", 'rain_mm']
            weather_df_list.append(weather)

    # concat pandas dataframes
    toronto_temperature = pd.concat(weather_df_list)

    return toronto_temperature

""" remove rain function, toronto weather temp function already contains rain data
def toronto_rain_2021():

    # list of pandas dataframes
    url = "https://ckan0.cf.opendata.inter.prod-toronto.ca/download_resource/12135710-2246-4df8-8aef-9bff7ae45357"
    req = requests.get(url)
    rain_raw = BytesIO(req.content)

    rain = pd.read_csv(rain_raw)
    rain.drop(columns=["id", "name", "longitude", "latitude"], inplace=True)
    rain["date"] = pd.to_datetime(rain["date"], format="%Y-%m-%dT%H:%M:%S")

    # avg 5 minute intervals from all rain gauges
    avg_rain = rain.groupby("date", as_index=False).agg("mean")
    # sum avged 5 min into 1 hour intervals
    avg_rain["date"] = pd.to_datetime(avg_rain["date"], format="%Y-%m-%dT%H").dt.floor(
        "H"
    )
    avg_rain = avg_rain.groupby("date", as_index=False).agg("sum")

    avg_rain.columns = ["ts", "rain_mm"]
    avg_rain["rain_mm"] = avg_rain["rain_mm"].round(2)

    return avg_rain
"""


def toronto_business_licence():
    """
    get toronto business license data as pandas dataframe
    """

    licence = pd.read_csv("https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/57b2285f-4f80-45fb-ae3e-41a02c3a137f/resource/54bddc5e-92d9-4102-89c1-43e82f8f4d2d/download/Business%20licences%20data.csv",
        encoding='latin1', 
        parse_dates=['Issued', 'Cancel Date', 'Last Record Update'],
        dtype={'Business Phone': 'object'},
        low_memory=False)
    
    # reorder columns to match database table
    licence.drop(columns=['_id'], inplace=True)
    cols = licence.columns.tolist()
    cols[0] , cols[1] = cols[1] , cols[0]
    licence = licence[cols]

    return licence


def toronto_water_use():
    """
    Get Toronto Daily Water Use Data Starting 2017
    Return as dataframe
    """
    url = 'https://www.toronto.ca/data/water/consumption/waterConsumption.json'
    water_raw = pd.read_json(url, convert_dates=['POSTED_DATE'])
    water = water_raw[['POSTED_DATE', 'TOR_DY_TOTAL']]
    water.dropna(inplace=True)
    water = water[(water['TOR_DY_TOTAL'] > 500) & (water['TOR_DY_TOTAL'] < 1500)]
    
    return water

def development_applications():
    """
    return toronto development applications data as dataframe
    """
    url = 'https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/0aa7e480-9b48-4919-98e0-6af7615b7809/resource/77f8a66a-bd43-40e6-b6c9-12a2b03a5032/download/Development%20Applications.csv'
    dev = pd.read_csv(url)
    dev = dev[dev['_id'].apply(lambda x: str(x).isdigit())]
    dev = dev[['_id', 'APPLICATION_TYPE', 'DATE_SUBMITTED', 'DESCRIPTION', 'POSTAL', 'STATUS', 'STREET_DIRECTION', 'STREET_NAME', 'STREET_NUM', 'STREET_TYPE', 'X', 'Y', 'APPLICATION#', 'REFERENCE_FILE#']]

    return dev

"""
def toronto_road_closure():

    try:
        # OpenWeather One Call API
        api_call = "https://secure.toronto.ca/opendata/cart/road_restrictions.json?v=2.0"
        response = requests.get(api_call)
        response.raise_for_status()

        # convert json to dictionary
        return response.json()

    except Exception as ex:
        raise ex

def toronto_road_closure_clean(road_closure=toronto_road_closure()):

    api_data = road_closure
    road_pd = pd.DataFrame(api_data['Closure'])
    road_close = road_pd[['road', 'latitude', 'longitude', 'startTime', 'endTime', 'description', 'type']]
    road_close['startTime'] = road_close['startTime'].astype('int').apply(lambda x: utc_to_local_time(x/1000))
    road_close['endTime'] = road_close['endTime'].astype('int').apply(lambda x: utc_to_local_time(x/1000))
    road_close['latitude'] = road_close['latitude'].astype(float)
    road_close['longitude'] = road_close['longitude'].astype(float)

    return road_close
"""