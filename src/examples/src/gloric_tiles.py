# %%
# ! pip install git+https://github.com/vga-team/py-lib.git
# ! pip install git+https://github.com/vga-team/gwf-vis_lib.git

# %% import
import vga
from gwfvis import conf as gwfvisconf
import json
import os

# %% basic config
GLORIC_DEMO_BASE_URL = "https://gwf-vis.usask.ca/assets/demo_gloric-app/app/"
vis_config = gwfvisconf.create_config()
vga.set_view(vis_config, center=[51, -116], zoom=5)
vga.set_prefer_canvas(vis_config, True)
vga.set_page_title(vis_config, "GWF-VIS GloRiC Tiles")
vga.set_favicon(
    vis_config,
    "https://assets-global.website-files.com/602eb43d42a3b5553a4f134c/6244bf4e6fe355c3bde76dbe_Favicon-32.png",
)

# %% import custom plugins
GL_LAYER_URL = f"{GLORIC_DEMO_BASE_URL}plugins/gl-layer.plugin.js"
GL_LAYER_NAME = "gloric-demo.gl-layer"
vga.import_plugin(vis_config, name=GL_LAYER_NAME, url=GL_LAYER_URL)

# %% add raster layer
raster_layer = vga.add_plugin(config=vis_config, name=gwfvisconf.PluginNames.TILE_LAYER)
vga.set_plugin_props(
    raster_layer,
    {
        "displayName": "Raster",
        "type": "overlay",
        "active": False,
        "urlTemplate": f"{GLORIC_DEMO_BASE_URL}tilesets/gloric_ca_raster/{{z}}/{{x}}/{{y}}.png",
    },
)


# %% add gl layer
gl_layer = vga.add_plugin(config=vis_config, name=GL_LAYER_NAME)
gl_layer_style = {  # https://maplibre.org/maplibre-style-spec/
    "version": 8,
    "sources": {
        "overlay": {
            "type": "vector",
            "tiles": [
                f"{GLORIC_DEMO_BASE_URL}tilesets/gloric_ca_vector/{{z}}/{{x}}/{{y}}.pbf"
            ],
            "errorTileURL": "data:application/x-protobuf;base64,",
            "minzoom": 1,
            "maxzoom": 6,
        }
    },
    "layers": [
        {
            "id": "overlay",
            "source": "overlay",
            "source-layer": "gloric",
            "type": "line",
            "paint": {
                "line-color": [
                    "case",
                    ["==", ["get", "Temp_av"], None],
                    "hsl(0, 100%, 30%)",
                    ["<=", ["get", "Temp_av"], 33.9],
                    "hsl(0, 100%, 100%)",
                    ["<=", ["get", "Temp_av"], 38.6],
                    "hsl(0, 100%, 95%)",
                    ["<=", ["get", "Temp_av"], 41.6],
                    "hsl(0, 100%, 90%)",
                    ["<=", ["get", "Temp_av"], 44.1],
                    "hsl(0, 100%, 85%)",
                    ["<=", ["get", "Temp_av"], 45.7],
                    "hsl(0, 100%, 80%)",
                    ["<=", ["get", "Temp_av"], 47.0],
                    "hsl(0, 100%, 75%)",
                    ["<=", ["get", "Temp_av"], 48.8],
                    "hsl(0, 100%, 70%)",
                    ["<=", ["get", "Temp_av"], 50.4],
                    "hsl(0, 100%, 65%)",
                    ["<=", ["get", "Temp_av"], 52.0],
                    "hsl(0, 100%, 60%)",
                    ["<=", ["get", "Temp_av"], 56.8],
                    "hsl(0, 100%, 55%)",
                    "hsl(0, 100%, 50%)",
                ],
                "line-opacity": 0.75,
                "line-width": [
                    "case",
                    ["==", ["get", "Log_spow"], None],
                    2,
                    ["<=", ["get", "Log_spow"], 2],
                    2,
                    ["<=", ["get", "Log_spow"], 3],
                    3,
                    ["<=", ["get", "Log_spow"], 4],
                    4,
                    ["<=", ["get", "Log_spow"], 5],
                    5,
                    6,
                ],
            },
        }
    ],
}
vga.set_plugin_props(
    gl_layer,
    {
        "displayName": "Vector",
        "type": "overlay",
        "active": True,
        "metadataStateKey": "gwf-default.metadata",
        "style": gl_layer_style,
        "eventLayerId": "overlay"
    },
)

# %% add metadata
metadata = vga.add_plugin(
    config=vis_config, name=gwfvisconf.PluginNames.METADATA, container="sidebar"
)

# %% option1: print the config JSON
print(json.dumps(vis_config))

# %% option2: print the URL
print(vga.generate_vis_url(vis_config))

# %% option3: save as a config file
config_directory = "../out"
config_file_name = "gloric_tiles.vgaconf"
if not os.path.exists(config_directory):
    os.makedirs(config_directory)
with open(f"{config_directory}/{config_file_name}", "w") as file:
    file.write(json.dumps(vis_config))

# %%
