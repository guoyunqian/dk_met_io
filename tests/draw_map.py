# -*- coding: utf-8 -*-

"""
Draw map.
"""

import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from dk_met_io.read_micaps import read_micaps_4

plt.rcParams['figure.figsize'] = (16, 12)


def plotMap():
    # Set the projection information
    proj = ccrs.LambertConformal(central_longitude=110.0, central_latitude=40, standard_parallels=[30])

    # Create a figure with an axes object on which we will plot. Pass the projection to that axes.
    fig, ax = plt.subplots(subplot_kw=dict(projection=proj))

    # Zoom in
    ax.set_extent([70, 140, 10, 60])

    # Add map features
    ax.add_feature(cfeature.LAND, facecolor='0.9')  # Grayscale colors can be set using 0 (black) to 1 (white)
    ax.add_feature(cfeature.LAKES, alpha=0.9)  # Alpha sets transparency (0 is transparent, 1 is solid)
    ax.add_feature(cfeature.BORDERS, zorder=10)
    ax.add_feature(cfeature.COASTLINE, zorder=10)

    # We can use additional features from Natural Earth (http://www.naturalearthdata.com/features/)
    states_provinces = cfeature.NaturalEarthFeature(
        category='cultural', name='admin_1_states_provinces_lines',
        scale='50m', facecolor='none')
    ax.add_feature(states_provinces, edgecolor='gray', zorder=10)

    # Add lat/lon grid lines every 20 to the map
    ax.gridlines(xlocs=np.arange(0, 360, 15), ylocs=np.arange(-90, 90, 10))

    return fig, ax


data = read_micaps_4('Z:/data/newecmwf_grib/pressure/17032008.006')
fig, ax = plotMap()
levels = np.arange(960, 1060, 5)
ax.contour(data['lon'], data['lat'], data.data, colors='k', levels=levels,
           linewidths=1, zorder=3, transform=ccrs.PlateCarree())
plt.tight_layout()
plt.show(block=True)
raw_input("Press Enter to continue...")

