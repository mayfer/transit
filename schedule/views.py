from django.http import HttpResponse
from transit.shortcuts import template_response
import queries
import formats

def stops(request):
    data = None
    return template_response('stops.html', data, request)

