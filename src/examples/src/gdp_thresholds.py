# %%
# ! pip install git+https://github.com/vga-team/py-lib.git
# ! pip install git+https://github.com/vga-team/gwf-vis_lib.git

# %% import
import vga
from gwfvis import conf as gwfvisconf, db as gwfvisdb
import json
import urllib.request
import os
import numpy as np

# %% config
vis_config = gwfvisconf.create_config()
vga.set_view(vis_config, center=[0, 0], zoom=2)
vga.set_page_title(vis_config, "GWF-VIS GDP (thresholds)")

# %% setup data provider
data_provider_plugin = vga.add_plugin(
    vis_config, name=gwfvisconf.PluginNames.SQLITE_LOCAL_DATA_PROVIDER
)
data_provider_plugin = vga.add_plugin(
    vis_config, name=gwfvisconf.PluginNames.GWFVISDB_DATA_PROVIDER
)


# %% download the gwfvisdb file
gwfvisdb_url = "https://gwf-vis.usask.ca/assets/datasets/gdp.gwfvisdb"
gwfvisdb_path = "../temp/_.gwfvisdb"
gwfvisdb_directory = os.path.dirname(gwfvisdb_path)
if not os.path.exists(gwfvisdb_directory):
    os.makedirs(gwfvisdb_directory)
urllib.request.urlretrieve(gwfvisdb_url, gwfvisdb_path)

# %% read the db file
options = gwfvisdb.read_gwfvis_db(gwfvisdb_path)

# %% calculate quantiles
values = options.values
values_for_variable = list(
    map(lambda x: x.value, filter(lambda x: x.variable.name == "GDP", options.values))
)
quantiles = [
    np.quantile(values_for_variable, 0),
    np.quantile(values_for_variable, 0.25),
    np.quantile(values_for_variable, 0.5),
    np.quantile(values_for_variable, 0.75),
    np.quantile(values_for_variable, 1),
]

# %% define color scheme
color_scheme = {
    "": {
        "type": "threshold",
        "scheme": ["blue", "green", "yellow", "red"],
        "thresholds": quantiles,
    }
}

# %% add GDP layer
data_source = f"gwfvisdb:{gwfvisdb_url}"
gdp_layer = vga.add_plugin(config=vis_config, name=gwfvisconf.PluginNames.GEOJSON_LAYER)
vga.set_plugin_props(
    gdp_layer,
    {
        "displayName": "GDP",
        "layerType": "overlay",
        "active": True,
        "colorScheme": color_scheme,
    },
)
# %% add data control
data_control = vga.add_plugin(
    config=vis_config,
    name=gwfvisconf.PluginNames.DATA_CONTROL,
    container="main",
    props={"dataSources": [data_source], "dataSourceDict": {"GDP": data_source}},
)

# %% add metadata
metadata = vga.add_plugin(
    config=vis_config,
    name=gwfvisconf.PluginNames.METADATA,
    container="sidebar",
    container_props={"slot": "top"},
)

# %% add line chart
metadata = vga.add_plugin(
    config=vis_config,
    name=gwfvisconf.PluginNames.LINE_CHART,
    container="sidebar",
    props={
        "dataFor": {
            "variableName": "GDP",
            "dimensionName": "time",
            "dataSource": data_source,
        },
        "locationLabelKey": "ADMIN",
    },
)

# %% option1: print the config JSON
print(json.dumps(vis_config))

# %% option2: print the URL
print(vga.generate_vis_url(vis_config))

# %% option3: save as a config file
config_directory = "../out"
config_file_name = "gdp_thresholds.vgaconf"
if not os.path.exists(config_directory):
    os.makedirs(config_directory)
with open(f"{config_directory}/{config_file_name}", "w") as file:
    file.write(json.dumps(vis_config))

# %%
