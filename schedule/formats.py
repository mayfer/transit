import json
import gtfs
from datetime import time, date, datetime

def dict_to_json(dict_obj):
	return json.dumps(dict_obj)

def to_dict(obj, classkey=None):
	if isinstance(obj, dict):
		for k in obj.keys():
			obj[k] = to_dict(obj[k], classkey)
		return obj
	elif hasattr(obj, "__iter__"):
		return [to_dict(v, classkey) for v in obj]
	elif hasattr(obj, "__dict__"):
		data = dict([(key, to_dict(value, classkey))
			for key, value in obj.__dict__.iteritems()
			if not callable(value) and not key.startswith('_')])
		if classkey is not None and hasattr(obj, "__class__"):
			data[classkey] = obj.__class__.__name__
		return data
	else:
		return obj

def format_time(dateobj):
	return dateobj.strftime("%I:%M %p")

def stop_to_dict(stop):
	dict_stop = {
		'id': stop.stop_id,
		'code': stop.stop_code,
		'name': stop.stop_name.title(),
		'description': stop.stop_desc.title(),
		'latitude': stop.stop_lat,
		'longitude': stop.stop_lon,
		#'routes': {}
	}
	if(stop.routes):
		dict_stop['routes'] = {}
		for stop_route in stop.routes:
			 route = {
				 'route_id': stop_route.route_id,
				 'full_name': stop_route.route_long_name.title(),
				 'trips': stop_route.times
			 }
			 dict_stop['routes'][stop_route.route_short_name] = route
	return dict_stop

def stop_to_json(stop):
	return dict_to_json(stop_to_dict(stop))

def stops_to_json(stops):
	dict_stops = []
	for stop in stops:
		dict_stops.append(stop_to_dict(stop))
	return dict_to_json(dict_stops)
	
def route_to_dict(route):
	dict_route = {
		'id': route.route_id,
		'short_name': route.route_short_name,
		'full_name': route.route_long_name.title(),
	}	 
	return dict_route

def routes_to_json(routes):
	dict_routes = []
	for route in routes:
		dict_routes.append(route_to_dict(route))
	return dict_to_json(dict_routes)

def stop_times_to_dict(stop_times):
	trips = []
	for stoptime in stop_times:
		trip = {}
		trip['time'] = format_time(gtfs.parse_stop_time(stoptime.departure_time))
		trip['trip_id'] = stoptime.trip_id
		trips.append(trip)
	return trips

def trip_to_dict(trip):
	dict_trip = {}
	dict_trip['trip_id'] = trip.trip_id
	dict_trip['headsign'] = trip.trip_headsign.title()
	dict_trip['route_id'] = trip.route.route_id
	dict_trip['stops'] = trip_stops_to_dict(trip.stops)
	return dict_trip

def trip_stops_to_dict(stop_times):
	stops = []
	for stoptime in stop_times:
		stop = {}
		stop['stop_id'] = stoptime.stop.stop_id
		stop['stop_name'] = stoptime.stop.stop_name.title()
		stop['latitude'] = stoptime.stop.stop_lat
		stop['longitude'] = stoptime.stop.stop_lon
		stop['time'] = format_time(gtfs.parse_stop_time(stoptime.departure_time))
		stops.append(stop)
	return stops