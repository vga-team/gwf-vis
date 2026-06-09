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
vga.set_view(vis_config, center=[0, 0], zoom=2)
vga.set_page_title(vis_config, "GWF-VIS GDP")

# %% setup data provider
data_provider_plugin = vga.add_plugin(
    vis_config, name=gwfvisconf.PluginNames.SQLITE_LOCAL_DATA_PROVIDER
)
data_provider_plugin = vga.add_plugin(
    vis_config, name=gwfvisconf.PluginNames.GWFVISDB_DATA_PROVIDER
)

# %% define color scheme
color_scheme = {"": {"type": "quantile", "scheme": ["blue", "green", "yellow", "red"]}}

# %% add GDP layer
data_source = "gwfvisdb:https://gwf-vis.usask.ca/assets/datasets/gdp.gwfvisdb"
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
config_file_name = "gdp.vgaconf"
if not os.path.exists(config_directory):
    os.makedirs(config_directory)
with open(f"{config_directory}/{config_file_name}", 'w') as file:
    file.write(json.dumps(vis_config))

# %%
