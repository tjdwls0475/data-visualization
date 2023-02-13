import requests
import openpyxl
import numpy as np
import seaborn
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from gmplot import gmplot
from geocoder import geocode_address

# Loading address values in the Excel files and appending these to Python list
file_path = r'./동탄 라이브오피스_사업환경-2.xlsx'
wb = openpyxl.load_workbook(file_path)
sheet = wb['화성시공급현황raw']
addresses = []
weights = []
latitudes = []
longitudes = []

for i in range(5,245):
    addresses.append(sheet['A' + str(i)].value)
    weights.append(sheet['D' + str(i)].value)

api_key = "XXX"

# Convert each address into a latitude and longitude
for address in addresses:
    latitude, longitude = geocode_address(address, api_key)
    latitudes.append(latitude)
    longitudes.append(longitude)
    
# Define the latitude and longitude of the center of the locations
center_lat = sum(latitudes) / len(latitudes)
center_lng = sum(longitudes) / len(longitudes)

# Create a gmplot instance and center the map on the first latitude and longitude point
gmap = gmplot.GoogleMapPlotter(center_lat, center_lng, zoom=11, apikey=api_key)

gradient = [
    (0, 0, 255, 0),  # blue with an alpha of 0 (fully transparent)
    (0, 0, 255, 0.5),  # blue with an alpha of 0.5 (semi-transparent)
    (0, 0, 255, 1)  # blue with an alpha of 1 (fully opaque)
]

# Plot the points on the map
gmap.heatmap(latitudes, longitudes, threshold=1, radius=30, opacity=0.3, dissipating=True, gradient=gradient)

# Save the map to an HTML file
gmap.draw("map-scatter.html")