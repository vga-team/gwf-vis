In this MESH example, the raw dataset is stored in the `raw` directory as a GIT submodule. 

## Workflow

1. Make sure the GIT submodule is checked out. If not, it can be checked out by using `git submodule update --init --recursive`.
1. Install the dependencies. A `requirement.txt` is provided.
1. Run `process_data.py`. It would generate a `mesh.gwfvisdb` file in the `out` directory.
1. Run `generate_vis.py`. It would generate a `mesh.vgaconf` file in the `out` directory.
1. Open `mesh.vgaconf` using the [VGA App](https://vga-team.github.io/app/), and select the `out` directory as the root directory. The vis should be shown up.
1. By selecting `MESH` from the data source dropdown of the data control, the features' shape should now be rendered on the map.
1. By selecting a variable from the variable dropdown, the features should be colored accroding to the color scheme.
1. By sliding or inputing the `time` dimension value, the colors of the features should be updated.
1. By clicking on a feature, the metadata and line chart would show relating info of the feature.
1. By clicking on the line chart, the timestamp of data control can be updated to the selected value.
