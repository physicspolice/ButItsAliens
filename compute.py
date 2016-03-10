from os.path import join, exists
from json import loads, dumps
from math import asin, sin
from csv import reader

# https://pypi.python.org/pypi/geographiclib
from geographiclib.geodesic import Geodesic
from geographiclib.constants import Constants

def sharpshooter(points):
	# TODO
	
	return []

# http://www.movable-type.co.uk/scripts/latlong.html#cross-track
def cross_track_distance(start, finish, target):

	# Earth's mean radius.
	R = Constants.WGS84_a

	# Geodesic from start to target.
	g = Geodesic.WGS84.Inverse(start[0], start[1], target[0], target[1])

	# Geodesic from start to finish.
	e = Geodesic.WGS84.Inverse(start[0], start[1], finish[0], finish[1])

	d13 = g['s12']  # Distance from start to target.
	b13 = g['azi1'] # Initial bearing from start to target.
	b12 = e['azi1'] # Initial bearing from start to finish.

	return abs(asin(sin(d13 / R) * sin(b13 - b12))) * R
	
	# TODO check against http://geo.javawa.nl/coordcalc/index_en.html calc #2

with open('sources.json') as file:
	sources = loads(file.read())

for name, url in sources.iteritems():
	path = join('sources', name.lower().replace(' ', '-') + '.csv')
	if not exists(path):
		print("Missing source file: %s" % path)
		continue
	with open(path) as file:
		csv = reader(file)
		csv.next() # Skip header row.
		points = [row for row in csv]
		for index, circle in enumerate(sharpshooter(points)):
			with open(join('data', str(index) + '.json'), 'w') as file:
				file.write(dumps({
					'name': name,
					'source': url,
					'equator': circle['equator'],
					'points': circle['points']
				}))
