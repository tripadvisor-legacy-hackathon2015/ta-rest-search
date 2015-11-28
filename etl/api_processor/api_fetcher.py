import urllib2
import json
import fileinput
import time
# list of ids from STDIN -> all relevant api info into files

def api_parser(file_name_location, location_info, review_info):

	data = json.loads(location_info)
	data_reviews = json.loads(review_info)

	review_array = []
	for review in data_reviews['data']:
		review_array.append(review['title'] + " " + review['text'])

	# prepare coordinates geo_point object
	coords = None
	if 'latitude' in data and 'longitude' in data:
		coords = {'lat': data['latitude'], 'lon': data['longitude']}

	# prepare address (if present)
	address = ''
	if 'address_obj' in data:
		address = data['address_obj']['address_string']
	
	# prepare rating (if present)
	rating = 0.0
	if 'rating' in data and data['rating']:
		rating = float(data['rating'])
		

	# filtering location to only fields we care about
	data_temp = {
				'placetype': "restaurant",
				'address': address,
				'coordinates': coords,
				'rating': rating,
				'name': data['name'],
				'price_level': data['price_level'],
				'reviews': review_array
				}

	with open(file_name_location, 'w') as outfile:
		json.dump(data_temp, outfile, indent=2)


def api_fetcher(id_list):

	for id in id_list:
		print(id)
		try:

			# reading api
			url = ('http://api.tripadvisor.com/api/partner/2.0/location/%s/?key=A9778200-77E7-4FD8-86B1-240E13A873F4' % id)
			location_info = urllib2.urlopen(url)
			location_info = location_info.read()

			# writing to file name
			file_name_location = str(id) + "_location.json"

			url = ('http://api.tripadvisor.com/api/partner/2.0/location/%s/reviews?key=A9778200-77E7-4FD8-86B1-240E13A873F4' % id)
			reviews_info = urllib2.urlopen(url)
			reviews_info = reviews_info.read()
			api_parser(file_name_location, location_info, reviews_info)

		except Exception as e:
			print("ERR: %s" % e)
			print(location_info)
			time.sleep(3)
			continue

id_list = []

for line in fileinput.input():
	id_list.append(line.strip())

api_fetcher(id_list)
