# PolygonOrthogonalSlicer
Takes input shapefile of polygons, and slices them in 1 of the 8 main cardinal directions (N,NE,E,SE,S,SW,W,NW). Script explains what the shapefile database needs to include. 
#Input table should have, at least, the following features with following headers:
#startx and starty are the centroid of your shape, or from whatever point you want the apex of the slice
    # |Direction|   startx  |   starty  |   geom
    # |---------|-----------|-----------|---------------- 
    # |   S     |-95.7958236|39.90223705|MULTIPOLYGON(((-95.787895...
    # |---------|-----------|-----------|----------------  
    # |   NE    |   ...     |   ...     |   ...
    # |---------|-----------|-----------|----------------
    # |   SW    |   ...     |   ...     |   ...
    # |---------|-----------|-----------|----------------

Non-routine code at the start of the script for a special case I was working on. Some editing needs to be done to remove this extraneous code for general use.
