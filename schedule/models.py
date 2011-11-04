from django.db import models

class Stop(models.Model):
    class Meta:
        db_table = 'stops'
    stop_id = models.IntegerField(primary_key=True)
    stop_code = models.IntegerField(null=True, db_index=True)
    stop_name = models.CharField(max_length=200, null=True, db_index=True)
    stop_desc = models.CharField(max_length=200, null=True, db_index=True)
    stop_lat = models.FloatField(null=True, db_index=True)
    stop_lon = models.FloatField(null=True, db_index=True)
    zone_id = models.IntegerField(null=True)
    stop_url = models.CharField(max_length=200, null=True)
    location_type = models.IntegerField(null=True)
    parent_station = models.CharField(max_length=200, null=True)
    routes = []
    def __unicode__(self):
        return self.stop_name


class Agency(models.Model):
    class Meta:
        db_table = 'agencies'
    agency_id = models.CharField(max_length=50, primary_key=True)
    agency_url = models.CharField(max_length=200, null=True)
    agency_name = models.CharField(max_length=200, null=True)
    agency_timezone = models.CharField(max_length=200, null=True)
    agency_lang = models.CharField(max_length=200, null=True)
    def __unicode__(self):
        return self.agency_name

	
class Route(models.Model):
    class Meta:
        db_table = 'routes'
    route_id = models.IntegerField(primary_key=True)
    agency = models.ForeignKey(Agency, null=True)
    route_short_name = models.CharField(max_length=10, null=True, db_index=True)
    route_long_name = models.CharField(max_length=200, null=True, db_index=True)
    route_desc = models.CharField(max_length=200, null=True)
    route_type = models.IntegerField(null=True)
    route_url = models.CharField(max_length=200, null=True)
    route_color = models.CharField(max_length=200, null=True)
    route_text_color = models.CharField(max_length=200, null=True)
    times = []
    def __unicode__(self):
        return self.route_short_name
        
class StopRoute(models.Model):
    class Meta:
        db_table = 'stop_routes'
    route = models.ForeignKey(Route)
    stop = models.ForeignKey(Stop)
    def __unicode__(self):
        return '{0} - {1}'.format(self.route.route_short_name, self.stop.stop_name)

class Shape(models.Model):
    class Meta:
        db_table = 'shapes'
    shape_id = models.IntegerField(primary_key=True)
    shape_pt_lat = models.FloatField(null=True)
    shape_pt_lon = models.FloatField(null=True)
    shape_pt_sequence = models.IntegerField(null=True)
    shape_dist_traveled = models.IntegerField(null=True)
    def __unicode__(self):
        return str(self.shape_id)
    
class Calendar(models.Model):
    class Meta:
        db_table = 'calendar'
    service_id = models.IntegerField(primary_key=True)
    monday = models.IntegerField(null=True)
    tuesday = models.IntegerField(null=True)
    wednesday = models.IntegerField(null=True)
    thursday = models.IntegerField(null=True)
    friday = models.IntegerField(null=True)
    saturday = models.IntegerField(null=True)
    sunday = models.IntegerField(null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    def __unicode__(self):
        return self.service_id
        
class CalendarDate(models.Model):
    class Meta:
        db_table = 'calendar_dates'
    service = models.ForeignKey(Calendar, null=True)
    date = models.DateField(null=True)
    exception_type = models.IntegerField(null=True)
    def __unicode__(self):
        return self.date

class Trip(models.Model):
    class Meta:
        db_table = 'trips'
    trip_id = models.AutoField(primary_key=True)
    route = models.ForeignKey(Route, null=True, db_index=True)
    service = models.ForeignKey(Calendar, null=True)
    trip_headsign = models.CharField(max_length=200, null=True)
    direction_id = models.IntegerField(null=True)
    block_id = models.IntegerField(null=True)
    shape = models.ForeignKey(Shape, null=True)
    stops = []
    def __unicode__(self):
        return self.trip_headsign

	
class StopTime(models.Model):
    class Meta:
        db_table = 'stop_times'
    stop_time_id = models.AutoField(primary_key=True)
    trip = models.ForeignKey(Trip, null=True, db_index=True)
    stop = models.ForeignKey(Stop, null=True, db_index=True)
    arrival_time = models.CharField(max_length=20, null=True)
    departure_time = models.CharField(max_length=20, null=True)
    stop_sequence = models.IntegerField(null=True)
    stop_headsign = models.CharField(max_length=200, null=True)
    pickup_type = models.IntegerField(null=True)
    drop_off_type = models.IntegerField(null=True)
    shape_dist_traveled = models.CharField(max_length=200, null=True)
    def __unicode__(self):
        return "{0}, {1}".format(self.stop_id, self.departure_time)

"""
class Transfer(models.Model):
    class Meta:
        db_table = 'transfers'
    from_stop = models.ForeignKey(Stop, null=True)
    to_stop = models.ForeignKey(Stop, null=True)
    transfer_type = models.IntegerField(null=True)
    min_transfer_time = models.IntegerField(null=True)
    def __unicode__(self):
        return "{0} -> {1}".format(self.from_stop_id, self.to_stop_id)
"""
