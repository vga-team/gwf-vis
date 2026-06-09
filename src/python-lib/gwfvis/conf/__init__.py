import base64
import json
from dataclasses import dataclass


@dataclass
class PluginNames:
    SQLITE_LOCAL_DATA_PROVIDER = "gwf-default.sqlite-local-data-provider"
    GWFVISDB_DATA_PROVIDER = "gwf-default.gwfvisdb-data-provider"
    TEST_DATA_FETCHER = "gwf-default.test-data-fetcher"
    TILE_LAYER = "gwf-default.tile-layer"
    GEOJSON_LAYER = "gwf-default.geojson-layer"
    CONTOUR_LAYER = "gwf-default.contour-layer"
    VECTOR_GRID_LAYER = "gwf-default.vector-grid-layer"
    LEGEND = "gwf-default.legend"
    DATA_CONTROL = "gwf-default.data-control"
    METADATA = "gwf-default.metadata"
    MARKDOWN = "gwf-default.markdown"
    LOCATION_PIN = "gwf-default.location-pins"
    LINE_CHART = "gwf-default.line-chart"


_DEFAULT_PLUGIN_PATH = "https://vga-team.github.io/gwf-vis_default-plugins"
_RECOMMENDED_PLUGIN_IMPORTS = {
    PluginNames.SQLITE_LOCAL_DATA_PROVIDER: f"{_DEFAULT_PLUGIN_PATH}/sqlite-local-data-provider.plugin.js",
    PluginNames.GWFVISDB_DATA_PROVIDER: f"{_DEFAULT_PLUGIN_PATH}/gwfvisdb-data-provider.plugin.js",
    PluginNames.TEST_DATA_FETCHER: f"{_DEFAULT_PLUGIN_PATH}/test-data-fetcher.plugin.js",
    PluginNames.TILE_LAYER: f"{_DEFAULT_PLUGIN_PATH}/tile-layer.plugin.js",
    PluginNames.GEOJSON_LAYER: f"{_DEFAULT_PLUGIN_PATH}/geojson-layer.plugin.js",
    PluginNames.CONTOUR_LAYER: f"{_DEFAULT_PLUGIN_PATH}/contour-layer.plugin.js",
    PluginNames.VECTOR_GRID_LAYER: f"{_DEFAULT_PLUGIN_PATH}/vector-grid-layer.plugin.js",
    PluginNames.LEGEND: f"{_DEFAULT_PLUGIN_PATH}/legend.plugin.js",
    PluginNames.DATA_CONTROL: f"{_DEFAULT_PLUGIN_PATH}/data-control.plugin.js",
    PluginNames.METADATA: f"{_DEFAULT_PLUGIN_PATH}/metadata.plugin.js",
    PluginNames.MARKDOWN: f"{_DEFAULT_PLUGIN_PATH}/markdown.plugin.js",
    PluginNames.LOCATION_PIN: f"{_DEFAULT_PLUGIN_PATH}/location-pins.plugin.js",
    PluginNames.LINE_CHART: f"{_DEFAULT_PLUGIN_PATH}/line-chart.plugin.js",
}
_DEFAULT_FAVICON_URL = "https://gwf.usask.ca/images/logos/GWF_Globe.png"


def create_config(no_basemap=False):
    return {
        "imports": _RECOMMENDED_PLUGIN_IMPORTS,
        "pageTitle": "GWF-VIS",
        "favicon": _DEFAULT_FAVICON_URL,
        "plugins": (
            [
                {
                    "import": "gwf-default.tile-layer",
                    "container": "",
                    "props": {
                        "displayName": "World_Imagery",
                        "active": True,
                        "urlTemplate": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                        "options": {
                            "attribution": "Source: Esri, Maxar, Earthstar Geographics, and the GIS User Community"
                        },
                    },
                }
            ]
            if no_basemap == False
            else []
        ),
    }
