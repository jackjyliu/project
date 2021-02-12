from datetime import datetime, timezone
import pytz

def utc_to_local_time(utc_raw):
    """
    convert utc datetime string to toronto time
    """
    local_timezone = pytz.timezone("America/Toronto")
    utc_datetime = datetime.fromtimestamp(utc_raw, tz=timezone.utc)  
    local_datetime = utc_datetime.astimezone(local_timezone)

    return local_datetime


def current_local_time():
    """
    return current toronto time as python datetime with timezone
    """
    local_timezone = pytz.timezone("America/Toronto")
    current_utc_time = datetime.utcnow().replace(tzinfo=pytz.utc)
    current_local_time = current_utc_time.astimezone(local_timezone)

    return current_local_time