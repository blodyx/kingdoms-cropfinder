#!/usr/bin/python
# -*- coding: utf-8 -*-

import json, numpy, math
from urllib.request import urlopen

server = input("What server? : ")
key = urlopen('http://'+server+'.kingdoms.com/api/external.php?email=ia@farstad.se&siteName=www&siteUrl=http://farstad.se&public=false&action=requestApiKey')
key = json.load(key)
key = key[u'response'][u'privateApiKey']

res = urlopen('http://'+server+'.kingdoms.com/api/external.php?privateApiKey='+key+'&action=getMapData')
data = json.load(res)

r = int(data[u'response'][u'map'][u'radius'])

map = [[0 for x in range(2*r+1)] for y in range (2*r+1)]
counter = [[0 for x in range(2*r+1)] for y in range (2*r+1)]
oasisMap = [[0 for x in range(2*r+1)] for y in range (2*r+1)]


for x in range (0,(len(data[u'response'][u'map'][u'cells']))):
        x1 = int(data[u'response'][u'map'][u'cells'][x][u'x'])
        y1 = int(data[u'response'][u'map'][u'cells'][x][u'y'])
        t = data[u'response'][u'map'][u'cells'][x][u'resType']
        if t == u'3339':
                map[x1+r][y1+r] = int(9)

        elif t == u'11115':
                map[x1+r][y1+r] = int(15)

        elif t == u'0' and data[u'response'][u'map'][u'cells'][x][u'oasis'] != u'0':
                map[x1+r][y1+r] = int(data[u'response'][u'map'][u'cells'][x][u'oasis'])

        elif int(data[u'response'][u'map'][u'cells'][x][u'landscape']) > 15 or None:
                map[x1+r][y1+r] = int(-1)
#count oasis
for i in range(0, 2*r+1):
        for j in range(0, 2*r+1):
                if map[i][j] == 9 or map[i][j] == 15:
                        oas = [0, 0, 0]
                        for k in range(i-3, i+4):
                                for l in range(j-3, j+4):
                                        try:
                                                if map[k][l] == 11 or map[k][l] == 21 or map[k][l] == 31 or map[k][l] == 40:
                                                        oas.append(25)
                                                elif map[k][l] == 41:
                                                        oas.append(50)
                                        except IndexError:
                                                pass

                        oas = sorted(oas, reverse=True)
                        oasisMap[i][j] = oas[0]+oas[1]+oas[2]
                        map[i][j] = map[i][j]*1000+ oasisMap[i][j]

a = numpy.asarray(map)
a = numpy.rot90(a,1)
a.transpose()
string = '/var/www/html/travian/2' + server  +'.csv'
numpy.savetxt(string, a, fmt="%d", delimiter=",")
print("data saved to: ", string)
                                                  
