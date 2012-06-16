from models import *
from django.db import connection
from datetime import datetime, timedelta, date
import formats, gtfs

def search_routes(search):
    results = Route.objects.filter(route_short_name__icontains=search)
    if len(search) > 2:
        more_results = Route.objects.filter(route_long_name__icontains=search)
        results = results | more_results
    return results[:5]
        
def search_stops(search):
    return Stop.objects.filter(stop_name__icontains=search) | Stop.objects.filter(stop_desc__icontains=search)
    
def get_stops_within_bounds(lat_north, lat_south, lon_east, lon_west):
    stops = Stop.objects.filter(stop_lat__lte=lat_north, stop_lat__gte=lat_south, stop_lon__lte=lon_east, stop_lon__gte=lon_west)
    return stops
    
def get_stops_within_bounds_with_times(lat_north, lat_south, lon_east, lon_west):
    stops = get_stops_within_bounds(lat_north, lat_south, lon_east, lon_west)
    for stop in stops:
        stop.routes = get_routes_for_stop(stop.stop_id)
    return stops
    
def get_num_stops_within_bounds(lat_north, lat_south, lon_east, lon_west):
    num_stops = Stop.objects.filter(stop_lat__lte=lat_north, stop_lat__gte=lat_south, stop_lon__lte=lon_east, stop_lon__gte=lon_west).count()
    return num_stops

def get_all_stops():
    stops = Stop.objects.all()
    return stops
    
def get_routes_for_stop_deprecated(stop_id):
    routes = [ sr.route for sr in StopRoute.objects.filter(stop=stop_id) ]
    for route in routes:
        route.times = get_next_stop_times(stop_id, route.route_id)
    return routes

def get_stop_from_id(id):
    stop = Stop.objects.get(stop_id=id)
    stop.routes = get_routes_for_stop(id)
    return stop

def get_next_stop_times(stop_id, route_id, next_times=3):
    now = datetime.now()
    two_min_ago = now - timedelta(minutes=2)
    service_ids = get_service_ids_for_date()
    stop_times = StopTime.objects.filter(stop=stop_id, trip__route=route_id, trip__service__in=service_ids, departure_time__gt=gtfs.datetime_to_string(two_min_ago)).order_by('departure_time', 'stop_sequence')[0:next_times]
    # print connection.queries
    # TODO: show AM times as end of the previous day.
    times = formats.stop_times_to_dict(stop_times)
    return times
    
def get_schedule(stop_id, route_id, date=date.today()):
    service_ids = get_service_ids_for_date(date)
    stop_times = StopTime.objects.filter(stop=stop_id, trip__route=route_id, trip__service__in=service_id).order_by('departure_time', 'stop_sequence')
    times = formats.stop_times_to_dict(stop_times)
    return times
    
def get_service_ids_for_date(date=date.today()):
    days = {
        0: 'monday',
        1: 'tuesday',
        2: 'wednesday',
        3: 'thursday',
        4: 'friday',
        5: 'saturday',
        6: 'sunday'
    }
    day_of_week = days[date.weekday()]
    kwargs = {
        day_of_week: 1
    }
    service_ids = [ calendar.service_id for calendar in Calendar.objects.filter(**kwargs) ]
    return service_ids
    
def get_trip_from_id(trip_id):
    trip = Trip.objects.get(trip_id=trip_id)
    trip.stops = get_stops_for_trip(trip_id)
    return trip
    
def get_stops_for_trip(trip_id):
    service_ids = get_service_ids_for_date()
    stop_times = StopTime.objects.filter(trip__trip_id=trip_id, trip__service__in=service_ids).order_by('departure_time', 'stop_sequence')
    return stop_times

def get_routes_for_stop(stop_id):
    routes = Route.objects.raw("SELECT * FROM routes WHERE route_id IN (SELECT DISTINCT t.route_id FROM stop_times AS st LEFT JOIN trips AS t ON st.trip_id=t.trip_id WHERE stop_id = %s)", [stop_id])
    routes = list(routes)
    for route in routes:
        route.times = get_next_stop_times(stop_id, route.route_id)
    return routes
