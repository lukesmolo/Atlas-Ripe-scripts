#/usr/bin/env python

#Copyright (C) 2015 lukesmolo <lukesmolo@gmail.com>

#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

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

n_domains = 100

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



with open(fl) as data_file:
    data = json.load(data_file)
    for country in data:
        procede = False

        string = 'sites/'+country["country"]+"_sites"
        i = -1
        request = copy.deepcopy(req)
        request_done = {}
        for probes in country["probes"]:
            request["probes"][0]["value"]+=(str(probes[0])+",")
        request_done = {}
        request["probes"][0]["value"] = request["probes"][0]["value"][:-1]
        request["probes"][0]["requested"] = str(country["n_probes"])

        request_done['country'] = country['country']
        request_done['n_sites'] = 0
        request_done['sites'] = []


        procede = False;
        f = open(string, 'r')
        counter = counter + 1
        if resume == True and country['country'] != sys.argv[1]:
            continue
        for line in f:
            procede = False;
            i = i+1
            if i < n_domains:
                while procede == False:
                    #print (country["country"]+ " " + str(probes[0]) + " " +line.strip())
                    request["definitions"][0]["target"] = line.strip()
                    request["definitions"][0]["description"] = (str(country['country'])+","+line.strip())
                    if resume == True and line.strip() != sys.argv[2]:
                       break
                    else:
                        resume = False
	
                    procede = make_request(request)
                    if procede == -1:
                        i-=1
                    request_done['n_sites'] = i+1
                    request_done['sites'].append(request["definitions"][0]["target"])
                with open('requests_done/'+str(counter)+'.json', 'w') as outfile:
                    json_data = json.dump(request_done, outfile)

        all_requests_done.append(request_done)

        #json_data = json.dumps(all_requests_done)
        #print(json_data)
        #with open('all_requests_done.json', 'w') as outfile:
            #json.dump(all_requests_done, outfile)



