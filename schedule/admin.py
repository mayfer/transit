from django.contrib import admin
from transit.schedule.models import Stop, Agency, Route, StopRoute, Trip, StopTime

admin.site.register(Stop)
admin.site.register(Agency)
admin.site.register(Route)
admin.site.register(StopRoute)
admin.site.register(Trip)
admin.site.register(StopTime)
