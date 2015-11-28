#! /usr/bin/env python3

## Demo ES uploader: takes in a condensed restaurant json entry and formats a 'coordinates' field and uploads.

import sys
import requests
import json
import time
import argparse

BASEURL = "http://es-hack-2.dai.gl:9200"
INDEXNAME = "locationidx"

parser = argparse.ArgumentParser()
parser.add_argument('--url')
parser.add_argument('files', nargs='*')
args = parser.parse_args()

if args.url:
    # override default
    BASEURL = args.url

def fmt_response(resp):
    if not resp:
        return "null"
    return "%s : %s" % (resp.status_code, resp.text[:100])

def create_index():
    print("Creating index")
    res = requests.post(BASEURL + '/' + INDEXNAME)
    print(fmt_response(res))
    time.sleep(3)

def create_mapping():
    print("Creating mapping")
    mapping_props = {
        "properties": {
            "coordinates": {"type": "geo_point"}
        }
    }
    res = requests.post(BASEURL + '/%s/_mapping/location' % INDEXNAME, data=json.dumps(mapping_props))
    print(fmt_response(res))
    time.sleep(3)

create_index()
create_mapping()

for fname in args.files:
    print(fname)
    
    with open(fname, 'r') as infile:
        restaurant_obj = json.load(infile)
        
        try:
            res = requests.post(BASEURL + '/%s/location' % INDEXNAME, data=json.dumps(restaurant_obj))
            print(fmt_response(res))
        except Error as e:
            print("ERR: %s" % e)
        
        
        
