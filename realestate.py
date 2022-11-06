import requests
import openpyxl
import numpy as np
import seaborn
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Loading address values in the Excel files and appending these to Python list
file_path = r'C:\Users\...\XXXXXX.xlsx'
wb = openpyxl.load_workbook(file_path)
sheet = wb['YYYYYY']
addresses = []
weights = []

for i in range(5,245):
    addresses.append(sheet['A' + str(i)].value)
    weights.append(sheet['D' + str(i)].value)
    
# Getting latitude and longitude of address by using Google Maps API
api_key = 'ZZZZZZ'
pt = np.zeros((len(addresses), 3))

for idx in range(len(addresses)):
    req_url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + addresses[idx] + '&key=' + api_key
    res = requests.get(req_url)
    if res.status_code == 200:
        #data =res.json()['results'][0]['geometry']['location']['lat']
        #print(data)
        pt[idx][0] = res.json()['results'][0]['geometry']['location']['lat']
        pt[idx][1] = res.json()['results'][0]['geometry']['location']['lng']
        pt[idx][2] = weights[idx]
#print('lat: ', pt[0][0])
#print('long: ', pt[0][1])

data = pd.DataFrame(pt, columns=['latitude', 'longitude', 'weights'])

seaborn.kdeplot(data=data, x="latitude", y="longitude", weights=weights, fill=True,)
plt.show()
print(data)

"""
m = Basemap(projection='mill', resolution='c',
            #llcrnrlat=37.0, urcrnrlat=37.5,
            #llcrnrlon=126.5, urcrnrlon=127.3
            )
m.drawmapboundary(fill_color='#DDEEFF')
m.fillcontinents(color='#FFEEDD')
m.drawcoastlines(color='gray', zorder=2)
m.drawcountries(color='gray', zorder=2)
"""

img = plt.imread("./map-example.png")
seaborn.kdeplot(data=data, x="latitude", y="longitude", weights=weights, fill=True,)
plt.imshow(img)

plot = seaborn.kdeplot(data=data, x="latitude", y="longitude", weights=weights,
                       #fill=True,
                       )
plot.imshow(img, aspect=plot.get_aspect(), extent=plot.get_xlim() + plot.get_ylim(), zorder=0.5)
plt.savefig('result.png', dpi = 1200)
