from models import *
from string import split, strip
import datetime, time

def importer(txt_location, obj_type):
    classmap = {
        'Stop': Stop,
        'Agency': Agency,
        'Route': Route,
        'Shape': Shape,
        'Calendar': Calendar,
        'CalendarDate': CalendarDate,
        'Trip': Trip,
        'StopTime': StopTime,
    }

    print obj_type
    num_imports = 0
    file = open(txt_location, "r")
    output = ''
    fields = split(strip(file.readline()), ",")
    #print fields
    while 1:
        line = file.readline()
        if not line:
            break
        values_unkeyed = split(line, ",")
        values = {}
        for num in range(len(values_unkeyed)):
            values[fields[num]] = values_unkeyed[num].strip()
        #print values
        obj = classmap[obj_type]()
        for key, val in values.items():
            if obj_type == "Calendar" or obj_type == "CalendarDate":
                # need to convert date string 20100515 to 2010-05-15
                try:
                    val = datetime.datetime.strptime(val, "%Y%m%d").strftime("%Y-%m-%d")
                    #print "passed {0}".format(val)
                except ValueError:
                    val = val
                    #print "(for key {0}) caught {1}".format(key, val)
            obj.__dict__[key] = val if val else False
        try:
            obj.save()
        except ValueError:
            print obj
        num_imports += 1
        del obj
        del values
    file.close()
    return num_imports
    
def link_routes_to_stops():
    all_stops = Stop.objects.all()
    stop_count = 0
    route_count = 0
    for stop in all_stops:
        routes = Route.objects.raw("SELECT * FROM routes WHERE route_id IN (SELECT DISTINCT t.route_id FROM stop_times AS st LEFT JOIN trips AS t ON st.trip_id=t.trip_id WHERE stop_id = %s)", [stop.stop_id])
        print stop.stop_id
        for route in routes:
            print "\t{0} - {1}".format(route.route_id, route.route_short_name)
            link = StopRoute()
            link.route = route
            link.stop = stop
            link.save()
            route_count += 1
        stop_count += 1
    return "{0} stops and {1} routes inserted".format(stop_count, route_count)
    
        
def import_all():
    num_imports = 0;
    dirname = 'google_transit/'
#    num_imports += importer(dirname+"stops.txt", "Stop")
#    num_imports += importer(dirname+"agency.txt", "Agency")
#    num_imports += importer(dirname+"routes.txt", "Route")
#    num_imports += importer(dirname+"shapes.txt", "Shape")
#    num_imports += importer(dirname+"calendar.txt", "Calendar")
#    num_imports += importer(dirname+"calendar_dates.txt", "CalendarDate")
#    num_imports += importer(dirname+"trips.txt", "Trip")
    num_imports += importer(dirname+"stop_times.txt", "StopTime")
    print link_routes_to_stops()
    print num_imports
    return num_imports
    
def import_remaining():
    num_imports = 0;
    num_imports += importer("google_transit/trips.txt", "Trip")
    num_imports += importer("google_transit/stop_times.txt", "StopTime")
    return num_imports
