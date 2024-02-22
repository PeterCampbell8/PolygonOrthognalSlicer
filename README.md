# PolygonOrthogonalSlicer
Takes input shapefile of polygons, and slices them in 1 of the 8 main cardinal directions (N,NE,E,SE,S,SW,W,NW). Script explains what the shapefile database needs to include. 

#Input table should have, at least, the following features with following headers:

#startx and starty are the centroid of your shape, or from whatever point you want the apex of the slice
<table>
<thead>
<tr>
<th>Direction</th>
<th>   startx  </th>
<th>   starty  </th>
<th>   geom
</tr>
</thead>
<tbody>
<tr>
<td>   S     </td>
<td>-95.7958236</td>
<td>39.90223705</td>
<td>MULTIPOLYGON(((-95.787895...</td>
</tr>
<tr>
<td>   NE    </td>
<td>   ...     </td>
<td>   ...     </td>
<td>   ...     </td>
</tr>
<tr>
<td>   SW    </td>   
<td>   ...     </td>
<td>   ...     </td>
<td>   ...     </td>
</tr>
</tbody>
</table>


Non-routine code at the start of the script for a special case I was working on. Some editing needs to be done to remove this extraneous code for general use.
