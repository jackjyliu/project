"""
get latest 10 events for dashboard calendar
"""

from todata.data.sql.functions import sql_read

def calendar():

    # load latest 10 events from RDS
    sql_raw = sql_read('toronto',
                        """
                        select
                            substring(event_date::varchar, 6, 5) as short_date,
                            event_name
                        from toronto_calendar
                        where event_date >= current_date
                        order by event_date
                        limit 10;
                        """) 
    
    # convert list of tuples to dictionary with date as key and name as value
    calendar = list()

    for event in sql_raw:
        calendar_event = {'date': event[0], 'name': event[1]}
        calendar.append(calendar_event)

    return calendar