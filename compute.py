from os.path import join, exists
from json import loads, dumps
from math import asin, sin
from csv import reader

# https://pypi.python.org/pypi/geographiclib
from geographiclib.geodesic import Geodesic
from geographiclib.constants import Constants

N = 9                 # Minimum number of points.
D = 100000            # 100 kilometers in meters.
R = Constants.WGS84_a # Earth's mean radius in meters.

# http://www.movable-type.co.uk/scripts/latlong.html#cross-track
def cross_track_distance(start, finish, target):

	# Geodesic from start to target.
	g = Geodesic.WGS84.Inverse(start[0], start[1], target[0], target[1])

	# Geodesic from start to finish.
	e = Geodesic.WGS84.Inverse(start[0], start[1], finish[0], finish[1])

	d13 = g['s12']  # Distance from start to target.
	b13 = g['azi1'] # Initial bearing from start to target.
	b12 = e['azi1'] # Initial bearing from start to finish.

	return abs(asin(sin(d13 / R) * sin(b13 - b12))) * R

def save(name, url, start, finish, points):
	save.id += 1
	with open(join('data', str(save.id) + '.json'), 'w') as file:
		file.write(dumps({
			'name': name,
			'source': url,
			'start': start,
			'finish': finish,
			'points': points
		}))
save.id = 0

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
		points = []
		for row in csv:
			row[1] = float(row[1])
			row[2] = float(row[2])
			points.append(row)
		last_point = len(points) - 1
		for i in range(0, last_point - 1):
			for j in range(i + 1, last_point):
				start = points[i][1:]
				finish = points[j][1:]
				matches = []
				for i, p in enumerate(points):
					if cross_track_distance(start, finish, p[1:]) <= D:
						matches.append(p)
				if len(matches) >= N:
					save(name, url, start, finish, matches)
