import json, pprint
from urllib2 import urlopen


server = raw_input('What server:')
key = urlopen('http://'+server+'.kingdoms.com/api/external.php?email=ia@farstad.se&siteName=www&siteUrl=http://farstad.se&public=false&action=requestApiKey')
key = json.load(key)
key = key[u'response'][u'privateApiKey']

res = urlopen('http://'+server+'.kingdoms.com/api/external.php?privateApiKey='+key+'&action=getMapData')
data = json.load(res)

r = data[u'response'][u'map'][u'radius']
r = int(r)
#mapdata = json.load(data[u'response'][u'map'][u'cells'])
print('Radius of map: '+str(r))
#print mapdata
map = [[0 for x in range(2*r+1)] for y in range (2*r+1)]
oasisMap = [[0 for x in range(2*r)] for y in range (2*r)] #saves oasis bonus associated to map fields
ww_xCoord = [50, 22, -22, -50, -22, 22]
ww_yCoord = [0, -45, -45, 0, 45, 45]
flag = int(1)

for x in range (0,(len(data[u'response'][u'map'][u'cells'])-1)):
	x1 = int(data[u'response'][u'map'][u'cells'][x][u'x'])
	y1 = int(data[u'response'][u'map'][u'cells'][x][u'y'])
	t = data[u'response'][u'map'][u'cells'][x][u'resType']
	if t == u'3339':
		map[x1+r][y1+r] = int(9)

	elif t == u'11115':
		map[x1+r][y1+r] = int(15)

	elif t == u'0' and data[u'response'][u'map'][u'cells'][x][u'oasis'] != u'0':
		map[x1+r][y1+r] = int(data[u'response'][u'map'][u'cells'][x][u'oasis'])

        elif t == 0:
                map[x1+r][y1+r] = int(-1)




for i in range(0, 2*r):
	for j in range( 0, 2*r):
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
while(flag == 1):

	croppers = [0 for x in range(len(ww_xCoord))]
	goodCroppers = [0 for x in range(len(ww_xCoord))]

	r2 = int(raw_input('Enter a range in which you want to analyze field:'))
	for z in range(len(ww_xCoord)):
		x = ww_xCoord[z]+r
		y = ww_yCoord[z]+r

		for i in range(x-r2, x+r2):
			for j in range(y-r2, y+r2):
			    try:
				if map[i][j] == 9 or map[i][j] == 15:
					croppers[z] += 1
					if oasisMap[i][j] >= 100 and map[i][j] == 15:
						goodCroppers[z] += 1
			    except IndexError:
                                pass

	maxCroppers = max(croppers)
	index_maxCroppers = croppers.index(maxCroppers)
	bestCroppers = max(goodCroppers)
	index_bestCroppers = goodCroppers.index(bestCroppers)

	if index_bestCroppers == index_maxCroppers:
		print('The best place to settle is: ['+str(ww_xCoord[index_maxCroppers])+';'+str(ww_yCoord[index_maxCroppers])+']\n Availables croppers: '+str(maxCroppers)+' and good croppers: '+str(bestCroppers))

		x = ww_xCoord[index_maxCroppers]+r
		y = ww_yCoord[index_maxCroppers]+r

		for i in range(x-r2, x+r2):
			for j in range(y-r2, y+r2):
			    try:
				if map[i][j] == 15 and oasisMap[i][j] >= 100:# or map[i][j] == 15:
					print(str(map[i][j])+'c coordinates: ['+str(i-r)+';'+str(j-r)+'] and oasis bonus: '+str(oasisMap[i][j]))
			    except IndexError:
                                pass


	else:
		#print option with most croppers but not best cropppers
		print('The place with most croppers to settle is: ['+str(ww_xCoord[index_maxCroppers])+';'+str(ww_yCoord[index_maxCroppers])+']'
				'\nAvailables croppers: '+str(croppers[index_maxCroppers])+' and good croppers: '+str(goodCroppers[index_maxCroppers])+'\n')

		x = ww_xCoord[index_maxCroppers]+r
		y = ww_yCoord[index_maxCroppers]+r

		for i in range(x-r2, x+r2):
			for j in range(y-r2, y+r2):
				if map[i][j] == 15 and oasisMap[i][j] >= 100:# or map[i][j] == 15:
					print(str(map[i][j])+'c coordinates: ['+str(i-r)+';'+str(j-r)+'] and oasis bonus: '+str(oasisMap[i][j]))

		#print option with less croppers but the best ones
		print('\nThe place with most good croppers to settle is: ['+str(ww_xCoord[index_bestCroppers])+';'+str(ww_yCoord[index_bestCroppers])+']'
				'\nAvailables croppers: '+str(croppers[index_bestCroppers])+' and good croppers: '+str(goodCroppers[index_bestCroppers]))

		x = ww_xCoord[index_bestCroppers]+r
		y = ww_yCoord[index_bestCroppers]+r

		for i in range(x-r2, x+r2):
			for j in range(y-r2, y+r2):
			    try:
				if map[i][j] == 15 and oasisMap[i][j] >= 100:# or map[i][j] == 15:
					print(str(map[i][j])+'c coordinates: ['+str(i-r)+';'+str(j-r)+'] and oasis bonus: '+str(oasisMap[i][j]))
			    except IndexError:
                                pass



	flag = int(input('\nEnter 1 if you want to search again and change range, otherwise enter any number\n ->'))

