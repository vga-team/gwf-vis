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
vga.set_view(vis_config, center=[51.5, -107], zoom=7)
vga.set_prefer_canvas(vis_config, True)
vga.set_page_title(vis_config, "GWF-VIS GloRiC")

# %% define color scheme
color_scheme = {
    "gwfvisdb:https://gwf-vis.usask.ca/assets/datasets/gloric.gwfvisdb": {
        "": {
            "type": "quantile",
            "scheme": "schemeGnBu[9]",
        },
        "Temp_av": {
            "type": "quantile",
            "scheme": "schemeOrRd[9]",
        },
    },
}

# %% define data source
data_source = "gwfvisdb:https://gwf-vis.usask.ca/assets/datasets/gloric.gwfvisdb"
data_source_dict = {"GLORIC": data_source}

# %% setup data provider
data_provider_plugin = vga.add_plugin(
    vis_config, name=gwfvisconf.PluginNames.SQLITE_LOCAL_DATA_PROVIDER
)
data_provider_plugin = vga.add_plugin(
    vis_config, name=gwfvisconf.PluginNames.GWFVISDB_DATA_PROVIDER
)

#%%
tile_layer = vga.add_plugin(
    config=vis_config, name=gwfvisconf.PluginNames.TILE_LAYER
)
vga.set_plugin_props(
    tile_layer,
    {
        "displayName": "Street",
        "layerType": "base-layer",
        "active": True,
        "urlTemplate": "https://server.arcgisonline.com/arcgis/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}"
    },
)

# %% add GLORIC layer
gloric_layer = vga.add_plugin(
    config=vis_config, name=gwfvisconf.PluginNames.GEOJSON_LAYER
)
vga.set_plugin_props(
    gloric_layer,
    {
        "displayName": "GLORIC",
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
    props={
        "dataSources": [data_source],
        "dataSourceDict": data_source_dict,
        "enableSecondaryVariable": True,
        "enableTertiaryVariable": True,
        "primaryVariableLabel": "Variable (Fill)",
        "secondaryVariableLabel": "Variable (Stroke)",
        "tertiaryVariableLabel": "Variable (Stroke Weight)",
    },
)

# %% add markdown
iframe_src = (
    "https://gwf-vis.usask.ca"
)
markdown = vga.add_plugin(
    config=vis_config,
    name=gwfvisconf.PluginNames.MARKDOWN,
    container="sidebar",
    container_props={"slot": "top"},
    props={
        "header": "Info",
        "markdown": f'<iframe src="{iframe_src}" style="height: 100%; width: 100%; min-height: 500px;" />',
    },
)

# %% add metadata
metadata = vga.add_plugin(
    config=vis_config, name=gwfvisconf.PluginNames.METADATA, container="sidebar"
)

# %% add legend
legend = vga.add_plugin(
    config=vis_config,
    name=gwfvisconf.PluginNames.LEGEND,
    props={
        "enableSecondaryVariable": True,
        "enableTertiaryVariable": True,
        "colorScheme": color_scheme,
    },
    container="main",
    container_props={"width": "20rem"},
)

# %% option1: print the config JSON
print(json.dumps(vis_config))

# %% option2: print the URL
print(vga.generate_vis_url(vis_config))

# %% option3: save as a config file
config_directory = "../out"
config_file_name = "gloric.vgaconf"
if not os.path.exists(config_directory):
    os.makedirs(config_directory)
with open(f"{config_directory}/{config_file_name}", "w") as file:
    file.write(json.dumps(vis_config))

# %%
