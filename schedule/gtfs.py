from datetime import date, time, datetime, timedelta

def parse_stop_time(departure_time):
    parsed_time = None
    try:
        parsed_time = datetime.strptime(departure_time, "%H:%M:%S")
    except Exception:
        # gtfs says:
        ## For times occurring after midnight on the service date, 
        ## enter the time as a value greater than 24:00:00 in HH:MM:SS
        ## local time for the day on which the trip schedule begins.
        # so it causes out-of-bounds error. let's fix it.
        hms = departure_time.split(':')
        am_hour = int(hms[0]) - 24
        fixed_time = "{0}:{1}:{2}".format(am_hour, hms[1], hms[2])
        parsed_time = datetime.strptime(fixed_time, "%H:%M:%S") + timedelta(days=1)
    return parsed_time

def datetime_to_string(datetime_obj):
    return datetime_obj.strftime("%H:%M:%S")