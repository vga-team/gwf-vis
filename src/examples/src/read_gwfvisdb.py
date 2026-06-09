# %%
# ! pip install git+https://github.com/vga-team/py-lib.git
# ! pip install git+https://github.com/vga-team/gwf-vis_lib.git

# %% import
from gwfvis import db as gwfvisdb
import json
import urllib.request
import os


# %% download the gwfvisdb file
gwfvisdb_url = (
    "https://gwf-vis.usask.ca/assets/datasets/mesh.new.gwfvisdb"
)
gwfvisdb_path = "../temp/_.gwfvisdb"
gwfvisdb_directory = os.path.dirname(gwfvisdb_path)
if not os.path.exists(gwfvisdb_directory):
    os.makedirs(gwfvisdb_directory)
urllib.request.urlretrieve(gwfvisdb_url, gwfvisdb_path)

# %% read the db file
options = gwfvisdb.read_gwfvis_db(gwfvisdb_path)

# %% info
options.info

# %% locations
options.locations

# %% dimensions
options.dimensions

# %% variables
options.variables

# %% values
options.values

# %%
