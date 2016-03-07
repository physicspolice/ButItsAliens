$(document).ready(function()
{
	$google.maps.event.addDomListener(window, 'load', function()
	{
		var map = new google.maps.Map(document.getElementById('map'), {
			'zoom': 3,
			'center': { 'lat': 0, 'lng': -180 },
			'mapTypeId': google.maps.MapTypeId.TERRAIN
		});
		$.ajax({
			'url': 'library.json',
			'type': 'GET',
			'dataType': 'json',
			'success': function(response)
			{
				var link = $('<a />').text(response.url).attr('href', response.url);
				$('footer p').html(link);
				$('h3').text(response.name);
				var equator = new google.maps.Polyline({
					'path': response.equator,
					'geodesic': true,
					'strokeColor': '#FF0000',
					'strokeOpacity': 1.0,
					'strokeWeight': 2
				});
				equator.setMap(map);
				for(var i in response.points)
				{
					var point = response.points[i];
					var marker = new google.maps.Marker({
						'position': point.location,
						'map': map,
						'title': point.name
					});
				}
			}
		});
	});
});
