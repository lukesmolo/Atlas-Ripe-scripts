#/usr/bin/env python

import sys, traceback
import json
from pprint import pprint
import urllib2
import copy
import time

key = ""
url = "https://atlas.ripe.net/api/v1/measurement/?key=%s" % key

req = {
"definitions": [
    {
	"target": "",
	"af": 4,
	"timeout": 4000,
	"description": "",
	"protocol": "TCP",
	"resolve_on_probe": "false",
	"packets": 3,
	"size": 48,
	"firsthop": 1,
	"destination_option_size": 0,
	"port": 80,
	"paris": 16,
	"maxhops": 32,
	"hop_by_hop_option_size": 0,
	"dontfrag": "false",
	"type":	"traceroute"
        }
    ],
"probes": [
    {
        "value": "",
        "type": "probes",
        "requested": 2
        }
    ],
"is_oneoff": "true"
}
global procede


def make_request(request):
    r = urllib2.Request(url)
    r.add_header("Content-Type", "application/json")
    r.add_header("Accept", "application/json")
    json_data = json.dumps(request)

    ret = True
    try:
        conn = urllib2.urlopen(r, json_data, 1000000000)
        string = conn.read()
        print(string)
        with open("./requests_done/requests", "a") as myfile:
             myfile.write(string+'\n')
        ret = True
    except urllib2.HTTPError, error:
	ret = False
	err = json.load(error)
	code = err['error']['code']
	print "Atlas answer error:",(err['error']['code'])

	if code == 103:
           ret = False
           time.sleep(10)
	elif code == 104:
	  ret = -1

    except urllib2.URLError, error:
        ret = False
        print "ERROR: ", error
        time.sleep(10)
    return ret

fl = './query_probes.json';

list_probes = []
i = -1
request = {}

all_requests_done = []
request_done = {}
global counter
counter = -1
global resume
resume = False



if len(sys.argv) == 3:
    resume = True

with open(fl) as data_file:
    data = json.load(data_file)
    for country in data:
        procede = False

        string = 'sites/'+country["country"]+"_sites"
        i = -1
        request = copy.deepcopy(req)
        #pprint(line["country"])
        request_done = {}
        for probes in country["probes"]:
            request["probes"][0]["value"]+=(str(probes[0])+",")
        request_done = {}
        request["probes"][0]["value"] = request["probes"][0]["value"][:-1]
        request["probes"][0]["requested"] = str(country["n_probes"])

        #print(country["probes"])
        request_done['country'] = country['country']
        request_done['n_sites'] = 0
        request_done['sites'] = []

        procede = False;
        f = open(string, 'r')
        counter = counter + 1
        #print(country['country'])
        if country['country'] != sys.argv[1] and resume == True:
            continue
        for line in f:
            procede = False;
            i = i+1
            if i < 100:
                while procede == False:
                    request["definitions"][0]["target"] = line.strip()
                    request["definitions"][0]["description"] = (str(country['country'])+","+line.strip())
                    if line.strip() != sys.argv[2] and resume == True:
                       break
                    else:
                        resume = False
                    procede = make_request(request)
                    if procede == -1:
                        i=-1
                    request_done['n_sites'] = i+1
                    request_done['sites'].append(request["definitions"][0]["target"])
                with open('requests_done/'+str(counter)+'.json', 'w') as outfile:
                    json_data = json.dump(request_done, outfile)


        all_requests_done.append(request_done)

        #json_data = json.dumps(all_requests_done)
        #print(json_data)
        #with open('all_requests_done.json', 'w') as outfile:
            #json.dump(all_requests_done, outfile)



