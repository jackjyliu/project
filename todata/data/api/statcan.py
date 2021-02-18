"""
functions to access Statistics Canada Data API
"""

import requests


# select data sources to query
SOURCE = {
    'manufacturing_sales':{
        'info': 'manufacturing sales amounts for GTA',
        'unit': 'CAD',
        'productID': 16100011,
        'coordinate': '10.1.1.1.0.0.0.0.0.0',
        'table': 'statcan_manufacture',
        'column': 'sales'
    },
    'population':{
        'info': 'population estimates of Toronto on July 1 of each year',
        'unit': 'person',
        'productID': 17100139,
        'coordinate': '166.1.1.0.0.0.0.0.0.0',
        'table': 'statcan_population',
        'column': 'persons'
    },
    'gas_price':{
        'info': 'gas price of unleaded regular gasoline',
        'unit': 'cents',
        'productID': 18100001,
        'coordinate': '9.2.0.0.0.0.0.0.0.0',
        'table': 'statcan_gas_price',
        'column': 'cents'
    },
    'ei':{
        'info': 'number of people on income support in Toronto',
        'unit': 'person',
        'productID': 14100323,
        'coordinate': '167.1.1.1.0.0.0.0.0.0',
        'table': 'statcan_ei',
        'column': 'persons'
    }
}


def get_data_series(source=SOURCE, series=None, productID=None, coordinate=None, latestN=99999, raw=False):
    """
    Get StatCan data series using cube pid api.
    If series is defined in SOURCE, then input series name as parameter,
    else input productID and coordinate, find on StatCan website.
    Returns list of tuples (to convert to dataframe or insert into db)
    """

    API_URL = 'https://www150.statcan.gc.ca/t1/wds/rest/getDataFromCubePidCoordAndLatestNPeriods'

    # build API request
    if series is not None:
        params = [{
            "productId": source[series]['productID'],
            "coordinate": source[series]['coordinate'],
            "latestN": latestN
        }]

    else:
        params = [{
            "productId": productID,
            "coordinate": coordinate,
            "latestN": latestN
        }]

    # Call API
    try:
        response = requests.post(API_URL, json=params)
        response.raise_for_status()
        results = response.json()

        # return raw json file if requested
        if raw:
            return results

    except Exception as ex:
        raise ex
    
    # return data as list of tuples
    data_series = list()
    for point in results[0]['object']['vectorDataPoint']:
        date = point['refPerRaw'] or point['refPer']
        
        if point['value'] is None:
            continue
        
        sample = (date, point['value'] * 10 ** point['scalarFactorCode'])
        data_series.append(sample)
    
    return data_series