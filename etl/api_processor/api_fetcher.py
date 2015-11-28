import urllib2
import json
import fileinput
# list of ids -> all relevant api info into files

def api_parser(file_name_location, file_name_reviews):

	with open(file_name_location) as data_file:
		data = json.load(data_file)

	with open(file_name_reviews) as data_file:
		data_reviews = json.load(data_file)

	review_array = []
	for review in data_reviews['data']:
		review_array.append(review['title'] + " " + review['text'])

	# filtering location
	data_temp = {
				'placetype': "restaurant",
				'address': data['address_obj']['address_string'],
				'latitude': float(data['latitude']), 
				'longitude': float(data['longitude']), 
				'rating': float(data['rating']),
				'name': data['name'],
				'price_level': data['price_level'],
				'reviews': review_array
				}

	with open(file_name_location + '_condensed', 'w') as outfile:
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
			text_file = open(file_name_location, "w")
			text_file.write(location_info)
			text_file.close()

			url = ('http://api.tripadvisor.com/api/partner/2.0/location/%s/reviews?key=A9778200-77E7-4FD8-86B1-240E13A873F4' % id)
			reviews_info = urllib2.urlopen(url)
			reviews_info = reviews_info.read()

			# writing to file name
			file_name_reviews = str(id) + "_reviews.json"
			text_file = open(file_name_reviews, "w")
			text_file.write(reviews_info)
			text_file.close()

			api_parser(file_name_location, file_name_reviews)

		except:
			continue

id_list = []

for line in fileinput.input():
	id_list.append(line.strip())

# print(id_list)

# api_fetcher([8066533])
api_fetcher(id_list)



