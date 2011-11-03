from django.http import HttpResponse
from transit.shortcuts import template_response
import queries
import formats

def index(request):
    return template_response('api_examples.html', None, request)
    
def get_all_stops(request):
	stops = queries.get_all_stops()
	return HttpResponse(formats.stops_to_json(stops), mimetype='application/json')

def get_num_stops_within_bounds(request, n, s, e, w):
    num_stops = queries.get_num_stops_within_bounds(n, s, e, w)
    return HttpResponse(formats.dict_to_json({'num_stops': num_stops}), mimetype='application/json')
    
# N and S latitudes, E and W longitudes (decimal)
def get_stops_within_bounds(request, n, s, e, w):
    stops = queries.get_stops_within_bounds(n, s, e, w)
    return HttpResponse(formats.stops_to_json(stops), mimetype='application/json')
def get_stops_within_bounds_with_times(request, n, s, e, w):
    stops = queries.get_stops_within_bounds_with_times(n, s, e, w)
    return HttpResponse(formats.stops_to_json(stops), mimetype='application/json')
    
def get_stop_from_id(request, stop_id):
    stop = queries.get_stop_from_id(stop_id)
    return HttpResponse(formats.stop_to_json(stop), mimetype='application/json')

def search(request, input):
    results = {}
    results['routes'] = [ formats.route_to_dict(route) for route in queries.search_routes(input) ]
    if len(input) > 3:
        results['stops'] = [ formats.stop_to_dict(stop) for stop in queries.search_stops(input) ]
    return HttpResponse(formats.dict_to_json(results), mimetype='application/json')
    
def get_trip_from_id(request, trip_id):
    trip = formats.trip_to_dict(queries.get_trip_from_id(trip_id))
    return HttpResponse(formats.dict_to_json(trip), mimetype='application/json')