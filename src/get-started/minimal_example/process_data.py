# %% imports
from typing import Sequence
import os
from pathlib import Path
import csv
import json
from gwfvis import db as gwfvis_db

# %% configs
geojson_path = "./raw/features.geojson"
variable_1_path = "./raw/variable_1.csv"
variable_2_path = "./raw/variable_2.csv"
output_db_path = "./out/foo.gwfvisdb"

# %% read input files
features: Sequence = []
with open(geojson_path, "r") as file:
    features = json.load(file)["features"]

variable_1: Sequence = []
with open(variable_1_path, "r") as file:
    variable_1 = list(csv.reader(file))

variable_2: Sequence = []
with open(variable_2_path, "r") as file:
    variable_2 = list(csv.reader(file))

# %% dataset info
info = [gwfvis_db.Info(key="name", value="Minimal Example", label="Name")]

# %% locations
locations: Sequence[gwfvis_db.Location] = [
    gwfvis_db.Location(
        id=feature["id"], geometry=feature["geometry"], metadata=feature["properties"]
    )
    for feature in features
]

# %% dimensions
time_dimension = gwfvis_db.Dimension(id=0, name="time", size=5)
dimensions = [time_dimension]

# %% variables
mock_variable_1 = gwfvis_db.Variable(id=0, name="Variable 1", dimensions=dimensions)
mock_variable_2 = gwfvis_db.Variable(id=1, name="Variable 2", dimensions=dimensions)
variables = [mock_variable_1, mock_variable_2]

# %% values
values: Sequence[gwfvis_db.Value] = []
for i in range(len(locations)):
    location = locations[i]
    for j in range(time_dimension.size):
        values.append(
            gwfvis_db.Value(
                location=location,
                variable=mock_variable_1,
                value=variable_1[i][j],
                dimension_dict={time_dimension: j},
            )
        )
        values.append(
            gwfvis_db.Value(
                location=location,
                variable=mock_variable_2,
                value=variable_2[i][j],
                dimension_dict={time_dimension: j},
            )
        )

# %% generate db
output_dir_path = Path(output_db_path).parent
os.makedirs(output_dir_path, exist_ok=True)
gwfvis_db.generate_gwfvis_db(
    output_db_path,
    options=gwfvis_db.Options(
        info=info,
        locations=locations,
        dimensions=dimensions,
        variables=variables,
        values=values,
    ),
)

# %%
