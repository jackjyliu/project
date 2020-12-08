"""
collection of functions to pull toronto related data from public sources, cleaned, formatted and returned as pandas dataframe
"""

from datetime import datetime
import calendar
import pandas as pd
import requests
from io import BytesIO


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
        power_file = pd.read_csv(f'http://reports.ieso.ca/public/DemandZonal/PUB_DemandZonal_{year}.csv', skiprows=3)
        power_file['DateTime'] = pd.to_datetime(power_file['Date'] + ' ' + power_file['Hour'].add(-1).astype(str) + ':00:00')
        toronto_power = power_file[['DateTime', 'Toronto']].copy()
        toronto_power.columns = ['ts', 'power_use_mwh']

        power_df_list.append(toronto_power)

    # concat pandas dataframes
    toronto_power_df = pd.concat(power_df_list)

    return toronto_power_df


def toronto_daylight(start_year=datetime.today().year, end_year=datetime.today().year,path='data\daylight\\toronto_daylight.txt'):
    """
    return pandas dataframe of toronto daylight hours
    please enter start_year and end_year
    """
    # load daylight file
    daylight_raw = pd.read_csv(path, skiprows=2, sep='\s+', header='infer')
    daylight_raw['combined_date'] = daylight_raw.index.values +" "+ daylight_raw['Date'].map(str)

    # empty list for cleaned dataframes
    daylight_df_list = list()

    for year in range(start_year, end_year + 1):
        ys = str(year)
        daylight_temp = daylight_raw.copy()
        
        # delete Feb 29 from daylight temp df to avoid errors
        if not calendar.isleap(year):
            daylight_temp = daylight_temp[daylight_temp['combined_date'] != 'Feb 29']

        # covert to datetime format
        daylight_temp['date'] = pd.to_datetime(ys + " " + daylight_temp['combined_date'], format='%Y %b %d')
        daylight_temp['rise'] = pd.to_datetime(ys + " " + daylight_temp['combined_date'] + " " + daylight_temp['Rise'], format='%Y %b %d %H:%M')
        daylight_temp['set'] = pd.to_datetime(ys + " " + daylight_temp['combined_date'] + " " + daylight_temp['Set'], format='%Y %b %d %H:%M')

        daylight_clean = daylight_temp[['date', 'rise', 'set', 'Day']].copy()
        daylight_clean.columns = ['date', 'rise', 'set', 'hours']
        daylight_clean.reset_index(inplace=True, drop=True)

        daylight_df_list.append(daylight_clean)

    toronto_daylight_df = pd.concat(daylight_df_list)
    
    return toronto_daylight_df


def toronto_weather(start_year=datetime.today().year, end_year=datetime.today().year, station_id=31688):
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
            url = f"https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID={station_id}&Year={year}&Month={month}&Day=14&timeframe=1&submit= Download+Data"
            req = requests.get(url)
            weather_raw = BytesIO(req.content)
            
            weather = pd.read_csv(weather_raw)
            weather['DateTime'] = pd.to_datetime(weather['Date/Time'])
            weather = weather[['DateTime', 'Temp (°C)', 'Rel Hum (%)', 'Stn Press (kPa)']]
            weather.columns = ['ts', 'temp_c', 'rel_hum_pct', 'pressure_kpa']
            weather_df_list.append(weather)
    
    # concat pandas dataframes
    toronto_weather = pd.concat(weather_df_list)
    
    return toronto_weather