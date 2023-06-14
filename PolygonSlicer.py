###
#Cut input shapes into orthogonal slices
#Input table should have, at least, the following features with following headers:
    # |Direction|   startx  |   starty  |   geom
    # |---------|-----------|-----------|---------------- 
    # |   S     |-95.7958236|39.90223705|MULTIPOLYGON(((-95.787895...
    # |---------|-----------|-----------|----------------  
    # |   NE    |   ...     |   ...     |   ...
    # |---------|-----------|-----------|----------------
    # |   SW    |   ...     |   ...     |   ...
    # |---------|-----------|-----------|----------------
###
import geopandas as gpd
from shapely.geometry import  Polygon
import numpy as np
import math as m
import time
startT = time.time()

#1----------Creating my input table as seen above----------------1
# polygon = "VoronoiPolygons.shp"
attributes = "FILE PATH"

# polys = gpd.read_file(polygon)
attribs = gpd.read_file(attributes)

#Dict with city names and their respective polygon
# cityDict = dict(zip(polys.NAME, polys.geometry))

# #Adding geometries to the reference table described at the start of the script
# attribs['geometry'] = attribs['Place'].map(cityDict)

attribs = attribs.astype({'startx':'float', 'starty':'float'})
#Copying down all original attributes but wiping geometries for use later
slices = attribs.copy(deep=True)
slices['geometry'] = None
#1-----------------------------------------------1


#2---Find the hypotenuse of each shape's bounding box to establish a distance for the clipping shape---2
def AddHypotDistance(gpframe):
    bound = attribs.bounds

    bound = bound.fillna(0.0) #If the NaN values become a problem, turn them to zeros with this

#  Finds the Hypotenuse for each item's bounding box, and adds it in a new column Hypot 
#  Remember, these are in teh input's units, so here it's degrees
    gpframe['Hypot'] = ((bound['maxx']-bound['minx'])**2)+((bound['maxy']-bound['miny'])**2)
    gpframe['Hypot'] = gpframe['Hypot'].apply(np.sqrt, axis=1, raw=True)

    return gpframe

attribs = AddHypotDistance(attribs)
#2------------------------------------------------------------------------------------------2


#3----------Point creation-----------
#create the first of 3 points for the clipping triangle with the startx and starty
attribs['point1'] = attribs[['startx','starty']].apply(tuple,axis=1)

#we have distance of lines, now need 2 points that will form a triangle with point1 field

#Collection of the two angles needed for the 2 points for each orthoganol direction and the four quadrants
Rads = {'N':(m.pi*.75, m.pi*.25), 'NE':(m.pi*.375, m.pi*.125), 'E':(m.pi*.25, m.pi*1.75), 'SE':(m.pi*1.875, m.pi*1.625),
        'S':(m.pi*1.75, m.pi*1.25), 'SW':(m.pi*1.375, m.pi*1.125), 'W':(m.pi*1.25, m.pi*.75), 'NW':(m.pi*.875, m.pi*.625),
        'NEQ':(m.pi*.5, 0), 'NWQ':(m.pi, m.pi*.5), 'SWQ':(m.pi*1.5, m.pi), 'SEQ':(m.pi*1.5, 0)}

#Cos then sin for x,y
def MakePoint2(data):
    #x = hypotenuse  * cos(radians of desired direction)+ starting coords     ----- then repeated for sin
    x = data['Hypot']*m.cos(Rads[data['Direction']][0]) + data['startx']
    y = data['Hypot']*m.sin(Rads[data['Direction']][0]) + data['starty']
    return (x,y)

def MakePoint3(data):
    x = data['Hypot']*m.cos(Rads[data['Direction']][1]) + data['startx']
    y = data['Hypot']*m.sin(Rads[data['Direction']][1]) + data['starty']
    return (x,y)


attribs['point2'] = attribs.apply(MakePoint2, axis=1)
attribs['point3'] = attribs.apply(MakePoint3, axis=1)
#3--------------------------------------------------------------------------------


#4-------Slicing and writing to the file---------
# All of the points for the clipping object have been made. Now just to do the clipping
def PizzaCutter(data):
    #make a polygon out of the 3 created points
    coords = [data['point1'],data['point2'],data['point3']]
    overlay = Polygon(coords)
    
    #try to intersect the original geometry and the created one. Exception raised if the input is a Null geometry
    try:
        return data['geometry'].intersection(overlay)
    except:
        return None

#Run the pizza cutter through the base shapes to create the new ones
#Remember that 'slices' is a copy of the input table, but with empty geometries. This way fields are retained.
slices['geometry'] = attribs.apply(PizzaCutter, axis = 1)

#Save the slices table as a shapefile
slices.to_file("FILE PATH")

stopT = time.time()
print("Elapsed time:", stopT - startT)