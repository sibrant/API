import os
import requests
import json
from sentinelsat.sentinel import read_geojson, geojson_to_wkt
from pandas.io.json import json_normalize

#set wd

os.chdir('D:/OneDrive/Documents/Work/CloudFerro/Projects/DIAS_CAP/DataSearch/WRLD_190814')


# import json
geom = geojson_to_wkt(read_geojson('north.geojson'))

#set search parameters, change as desired
#example S2
args = {'collection': 'Sentinel2',
        'product': 'LEVEL2A',
        'startDate': '2019-01-01',
        'completionDate': '2019-12-31',
        #'geometry': geom,
        'status': '34'
        #'status': '31|32'
        #'status': 'all'
        }

args = {'collection': 'Sentinel3',
        'product': 'LEVEL1',
        'startDate': '2018-01-01',
        'completionDate': '2019-12-31',
        'geometry': geom,
        #'status': '0|34|37'
        #'status': '31|32'
        'status': 'all'
        }


#example S1
# args = {'collection': 'Sentinel1',
#         'product': 'SLC',
#         'startDate': '2018-01-01',
#         'completionDate': '2019-12-31',
#         'geometry': geom,
#         'status': 'all'
#         }

# set product, depending on collection 
if args['collection'] == 'Sentinel1':
    pro = 'productType'
elif args['collection'] == 'Sentinel2':
    pro = 'processingLevel'

# Add level2p to level2 searches
if args['product'] == 'LEVEL2A':
    args['product'] = 'LEVEL2A|LEVELL2A|LEVELL2AP|LEVEL2AP'
	
# set return paramaters  
page = 1
maxRecords = 2000
resp = 'json'

# create API query dictionary
input_data = {
    "maxRecords": maxRecords,
	"page": page,
    #pro : args['product'],
	"startDate": args['startDate'],
	"completionDate": args['completionDate'],
    #"geometry": geom,
    "status": args['status']
}

# Build query
query = f'''http://finder.creodias.eu/resto/api/collections/{args['collection']}/search.{resp}?'''

# Send request
session = requests.Session()
response = session.get(query, params=input_data)
response.close()

# Show results
r = json.loads(response.text)

r1 = r

#loop through
while r['properties']['itemsPerPage'] == 2000:
    
    page +=1
    
    print(page)
    
    i1 = {'page': page}
    
    input_data.update(i1)
          
    # Send request
    session = requests.Session()
    response = session.get(query, params=input_data)
    response.close()
    
    r = json.loads(response.text)
    
    r1['features'].extend(r['features'])
    
df = json_normalize(r1['features'])

#some statistics
cnts = df['properties.status'].value_counts()

#create histogram
import matplotlib.pyplot as plt
import timestring

df['date'] = df['properties.startDate'].apply(lambda x : timestring.Date(x).date)

st = df['properties.status'].unique()

t = df['properties.status'].value_counts().index

plt.figure(figsize=(10,5))
   
for i in t:
    # Subset to the status
    subset = df[df['properties.status'] == i]
    
    # Draw the density plot
    plt.hist(subset['date'], bins=365, label=i, alpha=0.7, log = True)
    plt.legend(prop={'size': 10})
    
 
    
    
#plot footprints
import pandas as pd
import geopandas as gpd
import shapely.wkt
import geoplot

from sentinelsat import geojson_to_wkt

crs = {'init': 'epsg:4326'}

#gdf with polygons
dtmp = pd.DataFrame(columns=['wkt'])

for i in range (len(r1['features'])):
    
    dtmp.loc[i] = geojson_to_wkt((r1["features"][i]["geometry"]))
    
geompol = dtmp['wkt'].map(shapely.wkt.loads)

gdfpol = gpd.GeoDataFrame(df, crs=crs, geometry=geompol)

gdfpol_sub = gdfpol[gdfpol['properties.status'] == 31]
 
#gdf with centroid points
pts =  pd.DataFrame(columns=['wkt'])

for i in range (len(r1['features'])):
    
    pts.loc[i] = geojson_to_wkt((r1["features"][i]['properties']["centroid"]))
    
geompts = pts['wkt'].map(shapely.wkt.loads)

gdfpts = gpd.GeoDataFrame(df, crs=crs, geometry=geompts)

gdfpts_sub = gdfpts[gdfpts['properties.status'] == 31]
   

#load sample data
path = gpd.datasets.get_path('naturalearth_lowres')
bgm = gpd.read_file(path)

bgm = bgm[bgm['name'].isin(['Netherlands', 'Germany'])]

#plots
ax = geoplot.polyplot(gdfpol, edgecolor='red')
geoplot.polyplot(bgm, ax=ax)

f, ax = plt.subplots(1)
# Plot polygons in light grey
gpd.plotting.plot_polygon_collection(ax, bgm['geometry'], facecolor='grey', alpha=0.25, linewidth=0.1)

gpd.plotting.plot_polygon_collection(ax, gdfpol['geometry'], facecolor=None, edgecolor='green', linewidth=0.1)

f

geoplot.polyplot(f, ax=ax)

ax = geoplot.kdeplot(gdfpts_sub, shade=True, shade_lowest=False, 
                     cmap="coolwarm", clip = bgm.geometry)
geoplot.polyplot(bgm, ax=ax)



ax = geoplot.pointplot(gdfpts_sub)
geoplot.polyplot(bgm, ax=ax)


#optionally write away info
df['properties.title'].to_csv('NLD_S2-L2_st31_190626.csv', index= False)    
    


