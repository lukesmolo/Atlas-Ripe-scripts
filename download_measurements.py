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
import os

global n_measurement
n_measurement = 0

key = ''
url = 'https://atlas.ripe.net/api/v1/measurement/%d/?key=%s&format=json' % (n_measurement,key)

fl = './requests';

resume = False 

if len(sys.argv) == 2:
	resume = True


f = open(fl, 'r')
for line in f:
    country = None
    procede = False
    data = json.loads(line.strip())
    n_measurement = int(data['measurements'][0])
    if resume == True and n_measurement < int(sys.argv[1]):
	continue

    print(n_measurement)
    url = 'https://atlas.ripe.net/api/v1/measurement/%d/?key=%s&format=json' % (n_measurement,key)
    while procede == False:
        try:
            data = urllib2.urlopen(url).read()
            procede = True
        except urllib2.HTTPError, error:
            procede = False
        except urllib2.URLError, error:
            procede = False

    data = json.loads(data)
    name = data['description']
    country = data['description'][:2]
    print(country)

    directory = './'+country
    if (os.path.exists(directory)) == False:
        os.makedirs(directory)
    url = "https://atlas.ripe.net/api/v1/measurement/%d/result/" % n_measurement
    procede = False
    while procede == False:
        try:
            data = urllib2.urlopen(url).read()
            procede = True
        except urllib2.HTTPError, error:
            procede = False
        except urllib2.URLError, error:
            procede = False
    data = json.loads(data)

    with open(directory+'/'+name+'.json', 'w') as outfile:
            json.dump(data, outfile)


