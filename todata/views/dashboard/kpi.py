from datetime import datetime
from todata.data.utils.datetime import current_local_time
from todata.data.sql.functions import sql as psql


KPI_SUM = {
    "power use": {
        "kpi_title": "Power Use",
        "unit": "GigawattHour",
        "scaling": -3,
        "table": "power_demand",
        "date": "ts",
        "measure": "power_use_mwh",
    },
    "water use": {
        "kpi_title": "Water Use",
        "unit": "GigaLitre",
        "scaling": -3,
        "table": "water_use",
        "date": "ts",
        "measure": "water_megalitre",
    },
    "ei": {
        "kpi_title": "EI Recipients",
        "unit": "k persons",
        "scaling": -3,
        "table": "statcan_ei",
        "date": "series_date",
        "measure": "persons",
    },
    "manufacture": {
        "kpi_title": "GTA Manufacturer Sales",
        "unit": "Million$",
        "scaling": -6,
        "table": "statcan_manufacture",
        "date": "series_date",
        "measure": "sales",
    },
    "retail": {
        "kpi_title": "GTA Retail Sales",
        "unit": "Million$",
        "scaling": -6,
        "table": "statcan_retail",
        "date": "series_date",
        "measure": "sales",
    },
    "housing_starts": {
        "kpi_title": "GTA Housing Starts",
        "unit": "units",
        "scaling": 0,
        "table": "statcan_housing_starts",
        "date": "series_date",
        "measure": "units",
    },
    "flights": {
        "kpi_title": "YYZ Flights",
        "unit": "flights",
        "scaling": 0,
        "table": "statcan_flights",
        "date": "series_date",
        "measure": "flights",
    },
}

KPI_COUNT = {
    "business licence": {
        "kpi_title": "New Business Licence",
        "unit": "licences issued",
        "scaling": 0,
        "table": "business_licence",
        "date": "issued_date",
        "measure": "licence_no",
    },
    "development application": {
        "kpi_title": "Real Estate Development Application",
        "unit": "applications",
        "scaling": 0,
        "table": "development_application",
        "date": "date_submit",
        "measure": "DISTINCT application_num",
    },
}


def percent_format(decimal):

    plus_sign = ""
    if decimal > 0:
        plus_sign = "+"
    percent = plus_sign + str(int(decimal * 100)) + "%"

    return percent


def month_format(kpi_date):

    month = kpi_date.strftime("%Y.%m")

    return month

def trend(mom):
    if mom > 0:
        trend = 'up'
    elif mom < 0:
        trend = 'down'
    else:
        trend = 'flat'

    return trend


def kpi_month_sum(sql, table, date, measure, database="toronto"):
    
    record = sql.read_pd(
        f"""
        SELECT date_trunc('month', {date}) as month, SUM({measure}) as measure
        FROM {table}
        WHERE {date} < CURRENT_TIMESTAMP
        GROUP BY date_trunc('month', {date})
        ORDER BY month DESC
        LIMIT 14
        """
    )

    # check if latest data is from current incomplete month
    now = current_local_time()
    if datetime(year=now.year, month=now.month, day=1) <= datetime(
        year=record["month"][0].year, month=record["month"][0].month, day=1
    ):
        record = record[1:]

    latest_kpi = record["measure"].iloc[0]
    kpi_date = record["month"].iloc[0]
    mom = record["measure"].iloc[0] / record["measure"].iloc[1] - 1
    yoy = record["measure"].iloc[0] / record["measure"].iloc[12] - 1

    kpi = {
        "series": table,
        "measure": measure,
        "kpi_date": kpi_date,
        "latest_kpi": latest_kpi,
        "mom": mom,
        "yoy": yoy,
    }

    return kpi


def kpi_month_count(sql, table, date, measure, database="toronto"):

    record = sql.read_pd(
        f"""
        SELECT date_trunc('month', {date}) as month, COUNT({measure}) as measure
        FROM {table}
        WHERE {date} < CURRENT_TIMESTAMP
        GROUP BY date_trunc('month', {date})
        ORDER BY month DESC
        LIMIT 14
        """
    )

    # check if latest data is from current incomplete month
    now = current_local_time()
    if datetime(year=now.year, month=now.month, day=1) <= datetime(
        year=record["month"][0].year, month=record["month"][0].month, day=1
        ):
        record = record[1:]

    latest_kpi = record["measure"].iloc[0]
    kpi_date = record["month"].iloc[0]
    mom = record["measure"].iloc[0] / record["measure"].iloc[1] - 1
    yoy = record["measure"].iloc[0] / record["measure"].iloc[12] - 1
    
    kpi = {
        "series": table,
        "measure": measure,
        "kpi_date": kpi_date,
        "latest_kpi": latest_kpi,
        "mom": mom,
        "yoy": yoy,
    }

    return kpi


def kpi_package():

    package = list()
    sql = psql('toronto')

    for kpi in KPI_COUNT.values():
        result = kpi_month_count(sql, kpi["table"], kpi["date"], kpi["measure"])
        kpi_items = {
            "title": kpi["kpi_title"],
            "latest_kpi": int(result["latest_kpi"] * 10 ** kpi["scaling"]),
            "unit": kpi["unit"],
            "kpi_date": month_format(result["kpi_date"]),
            "mom": percent_format(result["mom"]),
            "yoy": percent_format(result["yoy"]),
            'trend': trend(result["mom"])
        }

        package.append(kpi_items)


    for kpi in KPI_SUM.values():
        result = kpi_month_sum(sql, kpi["table"], kpi["date"], kpi["measure"])
        kpi_items = {
            "title": kpi["kpi_title"],
            "latest_kpi": int(result["latest_kpi"] * 10 ** kpi["scaling"]),
            "unit": kpi["unit"],
            "kpi_date": month_format(result["kpi_date"]),
            "mom": percent_format(result["mom"]),
            "yoy": percent_format(result["yoy"]),
            'trend': trend(result["mom"])
        }

        package.append(kpi_items)
    
    sql.close()

    return package