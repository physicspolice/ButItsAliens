from os.path import join, exists
from json import loads, dumps
from csv import reader

def sharpshooter(points):
	# Do the texas sharpshooter thing.
	return []

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
