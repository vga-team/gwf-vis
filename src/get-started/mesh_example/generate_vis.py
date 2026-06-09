# %% imports
import vga
from gwfvis import conf as gwfvis_conf
import json
import os

# %% consts
# with this config, we should select the `out` directory as root directory when the vis loads
local_file_path = "mesh.gwfvisdb"

# %% create a vis_config and set some basic configs
vis_config = gwfvis_conf.create_config()
vga.set_view(vis_config, center=[51.3, -116], zoom=10)
vga.set_page_title(vis_config, "MESH Example")

# REQUEST LOCAL FILE ACCESS PERMISSION
vga.set_access_local_files(vis_config, True)

# %% set up the data providers
data_provider_plugin = vga.add_plugin(
    vis_config, name=gwfvis_conf.PluginNames.SQLITE_LOCAL_DATA_PROVIDER
)
data_provider_plugin = vga.add_plugin(
    vis_config, name=gwfvis_conf.PluginNames.GWFVISDB_DATA_PROVIDER
)

# %% add the vector layer into the vis
data_source = f"gwfvisdb:file:{local_file_path}"
vector_layer = vga.add_plugin(
    config=vis_config, name=gwfvis_conf.PluginNames.GEOJSON_LAYER
)
vga.set_plugin_props(
    vector_layer, {"displayName": "Foo", "layerType": "overlay", "active": True}
)

# %% add the data control
data_control = vga.add_plugin(
    config=vis_config,
    name=gwfvis_conf.PluginNames.DATA_CONTROL,
    container="main",
    props={
        "dataSources": [data_source],
        # just to give the data source a readable name "MESH"
        "dataSourceDict": {"MESH": data_source},
    },
)

# %% add the metadata display
metadata = vga.add_plugin(
    config=vis_config, name=gwfvis_conf.PluginNames.METADATA, container="sidebar"
)

# %% add a line chart showing the time-series data
metadata = vga.add_plugin(
    config=vis_config,
    name=gwfvis_conf.PluginNames.LINE_CHART,
    container="sidebar",
    props={
        "header": "Time",
        "dataFor": {"dimensionName": "time", "dataSource": data_source},
    },
)

# %% add a legend
legend = vga.add_plugin(
    config=vis_config,
    name=gwfvis_conf.PluginNames.LEGEND,
    container="main",
    container_props={"width": "20rem"},
)

# %% output option 1: print the config JSON
print(json.dumps(vis_config))

# %% output option 2: print the URL
print(vga.generate_vis_url(vis_config))

# %% output option 3: save as a config file
config_directory = "./out"
config_file_name = "mesh.vgaconf"
if not os.path.exists(config_directory):
    os.makedirs(config_directory)
with open(f"{config_directory}/{config_file_name}", "w") as file:
    file.write(json.dumps(vis_config))

# %%
