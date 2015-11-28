#! /usr/bin/env python3

## Demo ES uploader: takes in a condensed restaurant json entry and formats a 'coordinates' field and uploads.

import sys
import requests
import json
import time

BASEURL = "http://es-hack-2.dai.gl:9200"

def fmt_response(resp):
    if not resp:
        return "null"
    return "%s : %s" % (resp.status_code, resp.text[:100])

def create_index():
    print("Creating index")
    res = requests.post(BASEURL + '/locationidx')
    print(fmt_response(res))
    time.sleep(3)

def create_mapping():
    print("Creating mapping")
    mapping_props = {
        "properties": {
            "coordinates": {"type": "geo_point"}
        }
    }
    res = requests.post(BASEURL + '/locationidx/_mapping/location', data=json.dumps(mapping_props))
    print(fmt_response(res))
    time.sleep(3)

create_index()
create_mapping()

for fname in sys.argv[1:]:
    print(fname)
    
    with open(fname, 'r') as infile:
        restaurant_obj = json.load(infile)
        
        try:
            res = requests.post(BASEURL + '/locationidx/location', data=json.dumps(restaurant_obj))
            print(fmt_response(res))
        except Error as e:
            print("ERR: %s" % e)
        
        
        
