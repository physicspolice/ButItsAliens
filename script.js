var map;
var markers = [];
var equator;

function initialize()
{
	console.log('initialize');
	if(!map)
	{
		map = new google.maps.Map(document.getElementById('map'), {
			'zoom': 3,
			'center': { 'lat': 0, 'lng': -180 },
			'mapTypeId': google.maps.MapTypeId.TERRAIN
		});
	}
	if(markers)
	{
		for(var i = 0; i < markers.length; i++)
			markers[i].setMap(null);
		markers = [];
	}
	if(equator)
	{
		equator.setMap(null);
		equator = null;
	}

	$.ajax({
		'url': 'data/' + Math.floor((Math.random() * 5) + 1) + '.json',
		'type': 'GET',
		'dataType': 'json',
		'success': function(response)
		{
			var points = [];
			for(var i in response.points)
			{
				var p = response.points[i];
				points.push({'name': p[0], 'lat': p[1], 'lng': p[2]});
			}
			var link = $('<a />').text(response.url).attr('href', response.url);
			$('footer p').html(link);
			$('h3').text(response.name);
			equator = new google.maps.Polyline({
				'path': points,
				'geodesic': true,
				'strokeColor': '#FF0000',
				'strokeOpacity': 1.0,
				'strokeWeight': 2
			});
			equator.setMap(map);
			for(var i in points)
			{
				var point = points[i];
				var marker = new google.maps.Marker({
					'position': point,
					'map': map,
					'title': point.name
				});
				markers.push(marker);
			}
		}
	});
}

$(document).ready(function()
{
	$('button').click(initialize);
});
