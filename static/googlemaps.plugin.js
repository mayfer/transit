/* Murat Ayfer, http://muratayfer.com, 2011
 * Licensed under DWTFYW
 */
 
(function($){
	var init_defaults = {
		zoom: 12,
		center: new google.maps.LatLng(49.282364,-123.127384), // vancouver
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};

	var methods = {
		init: function(options) {
			return this.each(function() {
				if(!options) options = {};
				options.canvas = $(this).attr('id');
				var mapOptions = $.extend(init_defaults, options);
				data = {
					map: new google.maps.Map(document.getElementById(options.canvas), mapOptions),
					markers: [],
					infowindows: [],
					linePath: [],
					lineHandler: null,
				}
				$(this).data('googlemaps', data);
			});
		},
		addMarker: function(lat, lng, options) {
			data = $(this).data('googlemaps');
			options = $.extend({
				position: new google.maps.LatLng(lat, lng),
				map: data.map
			}, options);
			marker = new google.maps.Marker(options);
			data.markers.push(marker);
			return marker;
		},
		defineLine: function(lat, lng) {
			data = $(this).data('googlemaps');
			data.linePath.push(new google.maps.LatLng(lat, lng));
		},
		drawLine: function() {
			data = $(this).data('googlemaps');
			data.lineHandler = new google.maps.Polyline({
		        path: data.linePath,
		        strokeColor: "#5261a4",
		        strokeOpacity: 1.0,
		        strokeWeight: 2
        	});
        	data.lineHandler.setMap(data.map);
		},
		moveMarker: function(marker, lat, lng) {
			data = $(this).data('googlemaps');
			marker.setPosition(new google.maps.LatLng(lat, lng));
		},
		markerClicked: function(marker, callback) {
			google.maps.event.addListener(marker, 'click', callback);
		},
		markerHovered: function(marker, callbackIn, callbackOut) {
			google.maps.event.addListener(marker, 'mouseover', callbackIn);
			google.maps.event.addListener(marker, 'mouseout', callbackOut);
		},
		clear: function() {
			data = $(this).data('googlemaps');
			if(data.lineHandler) data.lineHandler.setMap(null);
			data.linePath = [];
			$.each(data.markers, function(i, marker) {
				marker.setMap(null);
			});
			$.each(data.infowindows, function(i, infowindow) {
				infowindow.close();
			});
			data.markers = [];
			data.infowindows = [];
		},
		getCenter: function() {
			data = $(this).data('googlemaps');
			var center = data.map.getCenter();
			return center;
		},
		setCenter: function(lat, lng) {
			data = $(this).data('googlemaps');
			data.map.panTo(new google.maps.LatLng(lat, lng));
		},
		zoom: function(zoom_val) {
			data = $(this).data('googlemaps');
			data.map.setZoom(parseInt(zoom_val));
		},
		getZoom: function() {
			data = $(this).data('googlemaps');
			return data.map.getZoom();
		},
		getBounds: function() {
			data = $(this).data('googlemaps');
			var bounds = data.map.getBounds();
			var ne = bounds.getNorthEast();
			var sw = bounds.getSouthWest();
			return {
				northeast: { lat: ne.lat(), lng: ne.lng() },
				southwest: { lat: sw.lat(), lng: sw.lng() }
			};
		},
		autoBounds: function() {
			data = $(this).data('googlemaps');
			if(data.markers.length) {
				var bounds = new google.maps.LatLngBounds();
				$.each(data.markers, function(i, marker) {
					bounds.extend(marker.getPosition());
				});
				data.map.fitBounds(bounds);
			}
		},
		infoWindow: function(marker, contentString, options) {
			data = $(this).data('googlemaps');
			options = $.extend({ content: contentString }, options);
			var infowindow = new google.maps.InfoWindow(options);
			google.maps.event.addListener(marker, 'click', function() {
				// close all other infowindows first
				$.each(data.infowindows, function(i, infowindow) {
					infowindow.close();
				});
				infowindow.open(data.map, marker);
			});
			data.infowindows.push(infowindow);
		},
		ajaxInfoWindow: function(marker, url, options) {
			data = $(this).data('googlemaps');
			options = $.extend({content: "<div class='map-loading'>Loading...</div>"}, options);
			var infowindow = new google.maps.InfoWindow(options);
			google.maps.event.addListener(marker, 'click', function() {
				// close all other infowindows first
				$.each(data.infowindows, function(i, infowindow) {
					infowindow.close();
				});
				infowindow.open(data.map, marker);
				$.get(url, function(data) {
					infowindow.setContent(data);
				});
			});
			data.infowindows.push(infowindow);
		},
		goToAddress: function(address) {
			data = $(this).data('googlemaps');
			if(!data.geocoder) data.geocoder = new google.maps.Geocoder();
			var result;
			data.geocoder.geocode( { 'address': address}, function(results, status) {
				if (status == google.maps.GeocoderStatus.OK) {
					if (status != google.maps.GeocoderStatus.ZERO_RESULTS) {
						data.map.setCenter(results[0].geometry.location);
					} else {
						alert("Address not found.");
					}
				} else {
					alert("Address not found.");
				}
			});
			return result;
		},
		mapMoving: function(callback) {
			data = $(this).data('googlemaps');
			google.maps.event.addListener(data.map, 'bounds_changed', callback);
		},
		mapReady: function(callback) {
			data = $(this).data('googlemaps');
			google.maps.event.addListener(data.map, 'idle', callback);
		},
		clearEvents: function() {
			data = $(this).data('googlemaps');
			google.maps.event.clearListeners(data.map, 'idle');
			google.maps.event.clearListeners(data.map, 'bounds_changed');
		}
	};

	$.fn.googlemaps = function(method) {
		if ( methods[method] ) {
			return methods[method].apply( this, Array.prototype.slice.call( arguments, 1 ));
		} else if ( typeof method === 'object' || ! method ) {
			return methods.init.apply( this, arguments );
		} else {
			$.error( 'Method ' +  method + ' does not exist on jQuery.googlemaps' );
		}
	};
})(jQuery);
