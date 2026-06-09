In this minimal example, the raw dataset is stored in the `raw` directory. In this directory, `features.geojson` stores the geometries and properties of two features. The mocked 5-timestamp time-series data are stored in `variable_1.csv` and `variable_2.csv` for two mocked variables respectively where each line is for a feature in `features.geojson`.

## Workflow

1. Install the dependencies. A `requirement.txt` is provided.
1. Run `process_data.py`. It would generate a `foo.gwfvisdb` file in the `out` directory.
1. Run `generate_vis.py`. It would generate a `foo.vgaconf` file in the `out` directory.
1. Open `foo.vgaconf` using the [VGA App](https://vga-team.github.io/app/), and select the `out` directory as the root directory. The vis should be shown up.
1. By selecting `Foo` from the data source dropdown of the data control, the features' shape should now be rendered on the map.
1. By selecting a variable from the variable dropdown, the features should be colored accroding to the color scheme.
1. By sliding or inputing the `time` dimension value, the colors of the features should be updated.
1. By clicking on a feature, the metadata and line chart would show relating info of the feature.
1. By clicking on the line chart, the timestamp of data control can be updated to the selected value.
