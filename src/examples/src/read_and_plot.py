# %%
# ! pip install git+https://github.com/vga-team/py-lib.git
# ! pip install git+https://github.com/vga-team/gwf-vis_lib.git
# ! pip install numpy==1.26.0
# ! pip install matplotlib==3.8.3
# ! pip install basemap==1.4.1

# %% import
from gwfvis import db as gwfvisdb
import json
import urllib.request
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


# %% download the gwfvisdb file
gwfvisdb_url = "https://gwf-vis.usask.ca/assets/datasets/stations.gwfvisdb"
gwfvisdb_path = "../temp/_.gwfvisdb"
gwfvisdb_directory = os.path.dirname(gwfvisdb_path)
if not os.path.exists(gwfvisdb_directory):
    os.makedirs(gwfvisdb_directory)
urllib.request.urlretrieve(gwfvisdb_url, gwfvisdb_path)

# %% read the db file
options = gwfvisdb.read_gwfvis_db(gwfvisdb_path)

# %% generate figure
def generate_figure():
    locations = options.locations

    geometries = list(map(lambda location: location.geometry, locations))
    xs = list(map(lambda geometry: geometry["coordinates"][0], geometries))
    ys = list(map(lambda geometry: geometry["coordinates"][1], geometries))

    fig = plt.figure(figsize=(8, 8))
    m = Basemap(projection='lcc', resolution=None,
                width=8E6, height=8E6, 
                lat_0=45, lon_0=-100)
    m.etopo(scale=0.5, alpha=0.5)
    m.scatter(xs, ys, latlon=True, alpha=0.5)
    fig.tight_layout(pad=0)

    return fig

generate_figure().show()

# %% save the plot as a file
out_directory = "../out"
out_file_name = "stations.jpg"
if not os.path.exists(out_directory):
    os.makedirs(out_directory)
generate_figure().savefig(f'{out_directory}/{out_file_name}')

# %%
