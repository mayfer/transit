// muratayfer.com 2011

var map;
var mode = 'stops';

$(document).ready(function() {
	var lat = $.cookie('lat');
	var lng = $.cookie('lng');
	var zm = $.cookie('zoom');
	var opts = {}
	if(lat && lng && zm) {
		opts = {
			zoom: parseInt(zm),
			center: new google.maps.LatLng(lat,lng)
		}
	}
    map = $('#map').googlemaps('init', opts);
    
    //map.googlemaps('geolocate');
    $('#search').submit(function(e) {
    	e.preventDefault();
    	map.googlemaps('goToAddress', $('#search-field').val()+" "+$('#city').val());
    	map.googlemaps('zoom', 16);
    	map.googlemaps('mapReady', updateStops);
    });
    $('.load-stops').live('click', function(e) {
    	e.preventDefault();
    	updateStops();
    });
    $('.back').live('click', function(e) {
    	e.preventDefault();
    	back();
    });
    map.googlemaps('mapReady', countStops);
});

function back() {
	var lat = $.cookie('lat');
	var lng = $.cookie('lng');
	var zm = $.cookie('zoom');
	if(lat && lng && zm) {
		map.googlemaps('setCenter', lat, lng);
		map.googlemaps('zoom', zm);
	}
	$('#map-controls-container').hide();
	stopsMode();
}

function updateStops() {
	if(mode!='stops') return;

	$('#map-controls-container').hide();
	$('#map-loader').show();
	var bounds = map.googlemaps('getBounds');
	var url = base_url+'api/stops/bounds/n/'+bounds.northeast.lat+'/s/'+bounds.southwest.lat+'/e/'+bounds.northeast.lng+'/w/'+bounds.southwest.lng+'/';
	$.getJSON(url, function(response) {
		map.googlemaps('clear');
		var marker_options;
		if(response.length > 200) {
			marker_options = {
				icon: new google.maps.MarkerImage(media_url + 'images/pin_small.png',
			      new google.maps.Size(10,10),
			      new google.maps.Point(0,0),
			      new google.maps.Point(5,5))
			}
		} else {
			marker_options = {
				icon: new google.maps.MarkerImage(media_url+'images/busstop.png',
			      new google.maps.Size(22,37),
			      new google.maps.Point(0,0),
			      new google.maps.Point(3,37)),
			    shadow: new google.maps.MarkerImage(media_url+'images/busstop_shadow.png',
			      new google.maps.Size(40,40),
			      new google.maps.Point(0,0),
			      new google.maps.Point(3,40)),
			}
		}
    	$.each(response, function(i,stop) {
            var marker = map.googlemaps('addMarker', stop.latitude, stop.longitude, marker_options);
            map.googlemaps('markerClicked', marker, function(){
	        	$('#map-loader').show();
            	var stop_url = base_url+'api/stop/'+stop.id+'/';
        		$('#main-title').html(stop.description);
        		if(stop.code) { $('#sub-title').html('#'+stop.code); }
        		else { $('#sub-title').html(''); }
        		$('table.bus-times .route').remove();
            	$.getJSON(stop_url, function(stop_response) {
            		$.each(stop_response.routes, function(j,route) {
            			var times = "";
	            		$.each(route.trips, function(k,trip) { times += "<a href='#' onclick='showTrip("+trip.trip_id+"); return false;' class='time'>" + remove_leading_zeros(trip.time) + "</a> "; });
	            		if(times=='') {
	            			times = "<span class='no-buses'>none today</span>";
	            		}
	            		var row = "<tr class='route'><td>"+remove_leading_zeros(j)+"</td><td>"+times+"</td></tr>";
	            		$('table.bus-times').append(row);
	            	});
	            	$('table.bus-times').show();
	        		$('#map-loader').hide();
            	});
            });
            map.googlemaps('markerHovered', marker, function(){
            	
            }, function(){
            	
            });
    	});
    	$('#map-loader').hide();
	});
}

function countStops() {
	if(mode!='stops') return;

	$('#map-loader').show();
	var bounds = map.googlemaps('getBounds');
	var url = base_url+'api/stops/count_within_bounds/n/'+bounds.northeast.lat+'/s/'+bounds.southwest.lat+'/e/'+bounds.northeast.lng+'/w/'+bounds.southwest.lng+'/';
	$.getJSON(url, function(response) {
		if(response.num_stops < 1000) {
			$('#map-controls-container').hide();
			var timer = setTimeout(updateStops, 1000);
			map.googlemaps('mapReady', function() { clearTimeout(timer) } );
		} else {
			$('#map-controls').html("Too many ("+response.num_stops+") stops in this area.<br />Zoom in or <a class='load-stops' href='#'>Show them anyway</a>");
			$('#map-controls-container').show();
			$('#map-loader').hide();
		}
	});
	var center = map.googlemaps('getCenter');
	var zoom = map.googlemaps('getZoom');
	$.cookie('lat', center.lat());
	$.cookie('lng', center.lng());
	$.cookie('zoom', zoom);
}

function showStopDetails() {
	
}

function showTrip(trip_id) {
   	$('#map-loader').show();
	tripMode();
	var url = base_url+'api/trip/'+trip_id+'/';
	map.googlemaps('clear');
	$.getJSON(url, function(response) {
		//alert(response.headsign);
		var marker_options = {
			icon: new google.maps.MarkerImage(media_url+'images/pin_small.png',
		      new google.maps.Size(10,10),
		      new google.maps.Point(0,0),
		      new google.maps.Point(5,5))
		};
		var path = [];
		$.each(response.stops, function(i,stop) {
			var marker = map.googlemaps('addMarker', stop.latitude, stop.longitude, marker_options);
			map.googlemaps('defineLine', stop.latitude, stop.longitude);
		});
		var poly = new google.maps.Polyline({
	        path: path,
	        strokeColor: "#5261a4",
	        strokeOpacity: 1.0,
	        strokeWeight: 2
    	});
    	poly.setMap(map.data('googlemaps').map);
    	map.googlemaps('drawLine');
		map.googlemaps('autoBounds');
		$('#map-controls').html("Showing full route for "+response.headsign+"<br /><a class='back' href='#'>Back to showing stops</a>");
		$('#map-controls-container').show();
		$('#map-loader').hide();
	});
}

function stopsMode() {
	map.googlemaps('clear');
	mode = 'stops';
	//map.googlemaps('mapReady', updateStops);
}
function tripMode() {
	mode = 'trip';
}
