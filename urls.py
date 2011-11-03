from django.conf.urls.defaults import *
from django.contrib import admin
import transit.settings as settings
import transit.schedule.api as api
import transit.schedule.views as views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.stops, name='index'),
    
    # web views
    url(r'^api/$', api.index, name='api'),
    
    # general api
    url(r'^api/search/([0-9a-zA-Z\s%_-]+)/$', api.search, name='search'),
    
    # stops
    url(r'^api/stop/(\d+)/$', api.get_stop_from_id, name='stop'),
    url(r'^api/stops/bounds/n/(-?\d+\.\d+)/s/(-?\d+\.\d+)/e/(-?\d+\.\d+)/w/(-?\d+\.\d+)/$', api.get_stops_within_bounds, name='stops-within-bounds'),
    url(r'^api/stops/bounds_with_times/n/(-?\d+\.\d+)/s/(-?\d+\.\d+)/e/(-?\d+\.\d+)/w/(-?\d+\.\d+)/$', api.get_stops_within_bounds_with_times, name='stops-within-bounds-with-times'),
    url(r'^api/stops/count_within_bounds/n/(-?\d+\.\d+)/s/(-?\d+\.\d+)/e/(-?\d+\.\d+)/w/(-?\d+\.\d+)/$', api.get_num_stops_within_bounds, name='num-stops-within-bounds'),
    url(r'^api/stops/all/$', api.get_all_stops, name='all-stops'),
    
    # routes
    url(r'^api/trip/(\d+)/$', api.get_trip_from_id, name='trip'),
    
    #(r'^test/(.*)/$', api.test),
    
    # Example:
    # (r'^transit/', include('transit.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

# to serve static files on development servers
if settings.DEBUG:
    from django.views.static import serve
    _media_url = settings.MEDIA_URL
    if _media_url.startswith('/'):
        _media_url = _media_url[1:]
        urlpatterns += patterns('',
            (r'^%s(?P<path>.*)$' % _media_url, serve, {'document_root': settings.MEDIA_ROOT})
        )
    del(_media_url, serve)