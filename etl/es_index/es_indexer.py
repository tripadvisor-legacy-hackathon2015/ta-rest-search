#! /usr/bin/env python3

## Demo ES uploader: takes in a condensed restaurant json entry and formats a 'coordinates' field and uploads.

import sys
import requests
import json

BASEURL = "http://es-hack-2.dai.gl:9200"

for fname in sys.argv[1:]:
    print(fname)
    
    with open(fname, 'r') as infile:
        restaurant_obj = json.load(infile)
    
    coord = {'lat': restaurant_obj['latitude'], 'lon': restaurant_obj['longitude']}
    post_req = {'coordinates': coord}
    for field in restaurant_obj.keys():
        if field in ['latitude', 'longitude']: continue
        
        post_req[field] = restaurant_obj[field]
    
    try:
        res = requests.post(BASEURL + '/locationidx/location', data=json.dumps(post_req))
        print(res.status_code)
    except Error as e:
        print("ERR: %s" % e)
        
        
        
