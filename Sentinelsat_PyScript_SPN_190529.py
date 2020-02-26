# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 11:25:59 2019

@author: sibra
"""

from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import matplotlib.pyplot as plt
import geopandas as gpd
import seaborn as sns
import pandas as pd
import os
import numpy as np
import array

os.chdir('D:/OneDrive/Documents/Work/CloudFerro/Projects/DIAS_CAP/DataSearch/SPN_S2_190325')

# connect to the API
api = SentinelAPI('dias_creotech', '4AfZ?tzs', 'https://cophub.copernicus.eu/dhus')
api = SentinelAPI('dias_creotech', '4AfZ?tzs', 'https://diashub2.copernicus.eu/dhus')
api = SentinelAPI('sibrant', 'sybsyb79', 'https://scihub.copernicus.eu/dhus')

  
# download single scene by known product id
#api.download(<product_id>)


#loop through S2 tile names to search complete Spain
tile = ['29TNH','29TPE','29TPF','29TQH','30STF','30STG','30STJ','30SWH','30SXG','30SXH','30SXJ','30TTK','30TTL','30TTM','30TUK','30TUL','30TUM','30TUN','30TVK','30TVL','30TVM','30TVN','30TWL','30TWM','30TWN','30TXK','30TXL','30TXM','30TXN','30TYK','30TYL','30TYM','30TYN','31TCF','31TCG']

#or Aragon
tile = ['31TCG','30TYN','30TYM','30TYL','30TYK','30TXN','30TXM','30TXL','30TXK','30TWM','30TWL']


#first search l2a data
gdfl2 = gpd.GeoDataFrame()
product = ['S2MSI2A', 'S2MSI2AP']

for i in tile:
    for j in product:
        productstmp = api.query(filename = '*%s*' % i,
                                beginPosition = ('20180101', '20181231'),
                                producttype = '%s' % j,
                                platformname = 'Sentinel-2')
        
        gdftmp = api.to_geodataframe(productstmp)
    
        gdfl2 = pd.concat([gdfl2, gdftmp], sort=True)
    
gdfl2.to_csv('SPN_l2a_18.csv')

   
#then search l1c data
gdfl1c = gpd.GeoDataFrame()

for i in tile:
    productstmp = api.query(filename = '*%s*' % i,
                            beginPosition = ('20160101', '20171231'),
                            producttype = 'S2MSI1C',
                            platformname = 'Sentinel-2')
    
    gdftmp = api.to_geodataframe(productstmp)
    
    gdfl1c = pd.concat([gdfl1c, gdftmp], sort=False) 
    
gdfl1c.to_csv('SPN_l1c_18_2.csv')

gdfl1c.title.to_csv('Aragon-L1C_160101-171231.txt', index= False, header = False)

                 
# download all results from the search
api.download_all(products)

# GeoJSON FeatureCollection containing footprints and metadata of the scenes
json = api.to_geojson(products)

# GeoPandas GeoDataFrame with the metadata of the scenes and the footprints as geometries


plt.hist(gdfl2['cloudcoverpercentage'], bins=100)

def getXY(pt):
    return (pt.x, pt.y)

gdf['centroid'] = gdf.geometry.centroid
gdf['x'] = gdf.geometry.centroid.x
gdf['y'] = gdf.geometry.centroid.y

cd = centroidseries.to_frame()

cd = pd.concat([to_frame(x),to_frame(y)], axis=1)
