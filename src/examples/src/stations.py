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
vga.set_view(vis_config, center=[51.3, -113], zoom=4)
vga.set_page_title(vis_config, "GWF-VIS GDP Weather Stations")

# %% setup data provider
data_provider_plugin = vga.add_plugin(
    vis_config, name=gwfvisconf.PluginNames.SQLITE_LOCAL_DATA_PROVIDER
)
data_provider_plugin = vga.add_plugin(
    vis_config, name=gwfvisconf.PluginNames.GWFVISDB_DATA_PROVIDER
)

# %% define color scheme
color_scheme = {
    "": {
        "type": "quantile",
        "scheme": "schemeOranges[5]",
    }
}

# %% add Station layer
data_source = 'gwfvisdb:https://gwf-vis.usask.ca/assets/datasets/stations.gwfvisdb'
station_layer = vga.add_plugin(
    config=vis_config, name=gwfvisconf.PluginNames.GEOJSON_LAYER
)
vga.set_plugin_props(
    station_layer, {"displayName": "MESH", "layerType": "overlay", "active": True, 'pointMode': 'circle', 'pointSize': 5, 'colorScheme': color_scheme}
)
# %% add data control
data_control = vga.add_plugin(
    config=vis_config,
    name=gwfvisconf.PluginNames.DATA_CONTROL,
    container="main",
    props={"dataSources": [data_source], "dataSourceDict": {"Stations": data_source}},
)

#%% add location pins
location_pin = vga.add_plugin(
    config=vis_config,
    name=gwfvisconf.PluginNames.LOCATION_PIN,
    container="sidebar",
    container_props={"slot": "top"},
)

# %% add metadata
metadata = vga.add_plugin(
    config=vis_config, name=gwfvisconf.PluginNames.METADATA, container="sidebar"
)

# %% add legend
legend = vga.add_plugin(
    config=vis_config,
    name=gwfvisconf.PluginNames.LEGEND,
    props={'colorScheme': color_scheme},
    container="main",
    container_props={"width": "20rem"},
)

# %% option1: print the config JSON
print(json.dumps(vis_config))

# %% option2: print the URL
print(vga.generate_vis_url(vis_config))

# %% option3: save as a config file
config_directory = "../out"
config_file_name = "stations.vgaconf"
if not os.path.exists(config_directory):
    os.makedirs(config_directory)
with open(f"{config_directory}/{config_file_name}", 'w') as file:
    file.write(json.dumps(vis_config))

# %%
