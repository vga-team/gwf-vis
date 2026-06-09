# %%
# ! pip install git+https://github.com/vga-team/py-lib.git
# ! pip install git+https://github.com/vga-team/gwf-vis_lib.git

# %% import
import vga
from gwfvis import conf as gwfvisconf
import json
import os

# %% config
vis_config = gwfvisconf.create_config()
vga.set_view(vis_config, center=[51.3, -116], zoom=10)
vga.set_page_title(vis_config, "GWF-VIS Color Config")

# %% setup data provider
data_provider_plugin = vga.add_plugin(
    vis_config, name=gwfvisconf.PluginNames.SQLITE_LOCAL_DATA_PROVIDER
)
data_provider_plugin = vga.add_plugin(
    vis_config, name=gwfvisconf.PluginNames.GWFVISDB_DATA_PROVIDER
)

# %% define color scheme
color_scheme = {
    "": {  # '' is for default (any variables that is not defined here)
        # here we use a quantize scale for custom array of colors
        "type": "quantize",
        "scheme": ["blue", "green", "yellow", "red"],
    },
    "scalarCanopyWat": {  # color definition for scalarCanopyWat only
        # here we use a quantile scale for custom array of colors
        "type": "quantile",
        "scheme": ["blue", "green", "yellow", "red"],
    },
    "scalarSWE": {  # color definition for scalarSWE only
        # here we use a sequential scale for custom array of colors
        "type": "sequential",
        "scheme": ["blue", "green", "yellow", "red"],
    },
    "scalarTotalIET": {  # color definition for scalarTotalIET only
        # here we use a quantize scale for builtin color scheme, the builtin scheme names can be found at https://github.com/d3/d3-scale-chromatic
        "type": "quantize",
        # use a single string instead of an array means to use the built in scheme
        "scheme": "schemeOranges[5]",
    },
    "scalarTotalRunoff": {  # color definition for scalarTotalRunoff only
        # here we use a sequential scale for builtin color scheme, the builtin scheme names can be found at https://github.com/d3/d3-scale-chromatic
        "type": "sequential",
        # use a single string instead of an array means to use the built in scheme, note that for sequntial, you have to use interpolate colors
        "scheme": "interpolateOranges",
    },
}

# %% add SUMMA layer
data_source = "gwfvisdb:https://gwf-vis.usask.ca/assets/datasets/catchment.gwfvisdb"
summa_layer = vga.add_plugin(
    config=vis_config, name=gwfvisconf.PluginNames.GEOJSON_LAYER
)
vga.set_plugin_props(
    summa_layer,
    {
        "displayName": "SUMMA",
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
    props={"dataSources": [data_source], "dataSourceDict": {"SUMMA": data_source}},
)

# %% add legend
metadata = vga.add_plugin(
    config=vis_config,
    name=gwfvisconf.PluginNames.LEGEND,
    container="main",
    props={"colorScheme": color_scheme},
    container_props={"width": "20rem"},
)

# %% option1: print the config JSON
print(json.dumps(vis_config))

# %% option2: print the URL
print(vga.generate_vis_url(vis_config))

# %% option3: save as a config file
config_directory = "../out"
config_file_name = "color_config.vgaconf"
if not os.path.exists(config_directory):
    os.makedirs(config_directory)
with open(f"{config_directory}/{config_file_name}", 'w') as file:
    file.write(json.dumps(vis_config))

# %%
