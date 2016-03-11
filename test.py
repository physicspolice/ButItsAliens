# TODO Check against calculation #2:
# http://geo.javawa.nl/coordcalc/index_en.html

from math import asin, sin

from geographiclib.geodesic import Geodesic
from geographiclib.constants import Constants

def cross_track_distance(start, finish, target):
	R = Constants.WGS84_a
	g = Geodesic.WGS84.Inverse(start[0], start[1], target[0], target[1])
	e = Geodesic.WGS84.Inverse(start[0], start[1], finish[0], finish[1])
	d13 = g['s12']
	b13 = g['azi1']
	b12 = e['azi1']
	return abs(asin(sin(d13 / R) * sin(b13 - b12))) * R

target = [52.20, 5.30]
start  = [52.10, 5.50]
finish = [52.26, 5.45]

print cross_track_distance(start, finish, target)
