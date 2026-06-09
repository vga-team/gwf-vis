# %% install
# ! pip install git+https://github.com/vga-team/py-lib.git
# ! pip install git+https://github.com/vga-team/gwf-vis_lib.git

# %% import
import vga
from gwfvis import conf as gwfvisconf
import json
import os

# %% config
vis_config = gwfvisconf.create_config()
vga.set_view(vis_config, center=[56.4, -123.2], zoom=6)
vga.set_page_title(vis_config, "GWF-VIS Permafrost")

# %% setup data provider
data_provider_plugin = vga.add_plugin(
    vis_config, name=gwfvisconf.PluginNames.SQLITE_LOCAL_DATA_PROVIDER
)
data_provider_plugin = vga.add_plugin(
    vis_config, name=gwfvisconf.PluginNames.GWFVISDB_DATA_PROVIDER
)

# %% define color scheme
thresholds = [20, 60, 120, 180, 250]

color_scheme = {
    "": {
        "type": "threshold",
        "thresholds": thresholds,
        "scheme": ["azure", "blue", "green", "yellow", "orange", "red"],
    }
}

# %% add permafrost layers
data_source = "gwfvisdb:https://gwf-vis.usask.ca/assets/datasets/permafrost-reduced-locations.gwfvisdb"
contour_layer = vga.add_plugin(
    config=vis_config,
    name=gwfvisconf.PluginNames.CONTOUR_LAYER,
    props={
        "colorScheme": color_scheme,
        "displayName": "Permafrost Contours",
        "lineWeight": 1,
        "opacity": 0.3,
        "layerType": "overlay",
        "active": True,
    },
)
point_layer = vga.add_plugin(
    config=vis_config,
    name=gwfvisconf.PluginNames.GEOJSON_LAYER,
    props={
        "colorScheme": color_scheme,
        "displayName": "Permafrost Points",
        "layerType": "overlay",
        "pointSize": 5,
        "active": False,
    },
)

# %% add location pins
metadata = vga.add_plugin(
    config=vis_config,
    name=gwfvisconf.PluginNames.LOCATION_PIN,
    container="sidebar",
    container_props={"slot": "top"},
)

# %% add data control
data_control = vga.add_plugin(
    config=vis_config,
    name=gwfvisconf.PluginNames.DATA_CONTROL,
    container="sidebar",
    props={"dataSources": [data_source], "dataSourceDict": {"Permafrost": data_source}},
    container_props={"slot": "top"},
)

# %% add line charts
line_chart_cycle = vga.add_plugin(
    config=vis_config,
    name=gwfvisconf.PluginNames.LINE_CHART,
    container="sidebar",
    props={
        "header": "cycle",
        "dataFor": {
            "dimensionName": "cycle",
            "dataSource": data_source,
            "variableNames": ["TSOL_MIN", "TSOL_MAX"],
        },
    },
)

line_chart_gru = vga.add_plugin(
    config=vis_config,
    name=gwfvisconf.PluginNames.LINE_CHART,
    container="sidebar",
    props={
        "header": "gru",
        "dataFor": {
            "dimensionName": "gru",
            "dataSource": data_source,
            "variableNames": ["TSOL_MIN", "TSOL_MAX"],
        },
    },
)

line_chart_level = vga.add_plugin(
    config=vis_config,
    name=gwfvisconf.PluginNames.LINE_CHART,
    container="main",
    props={
        "header": "level",
        "dataFor": {
            "dimensionName": "level",
            "dataSource": data_source,
            "variableNames": ["TSOL_MIN", "TSOL_MAX"],
        },
    },
    container_props={"width": "100vw"},
)


# %% add legend
legend = vga.add_plugin(
    config=vis_config,
    name=gwfvisconf.PluginNames.LEGEND,
    container="main",
    container_props={"width": "20rem"},
    props={
        "colorScheme": color_scheme,
    },
)

# %% option1: print the config JSON
print(json.dumps(vis_config))

# %% option2: print the URL
print(vga.generate_vis_url(vis_config))

# %% option3: save as a config file
config_directory = "../out"
config_file_name = "permafrost.vgaconf"
if not os.path.exists(config_directory):
    os.makedirs(config_directory)
with open(f"{config_directory}/{config_file_name}", "w") as file:
    file.write(json.dumps(vis_config))

# %%
