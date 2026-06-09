# %% imports
from typing import Sequence
import os
from pathlib import Path
import shapefile
import netCDF4 as nc
from gwfvis import db as gwfvis_db

# %% configs
metadata_fields = ["COMID", "unitarea"]
shape_file_path = (
    "./raw/MESH-Scripts/Model_Workflow/shapefiles/catchment/BowAtBanff_cat.shp"
)
rff_nc_file_path = "./raw/MESH-Scripts/Model_Workflow/vector_based_workflow/6_model_runs/results/RFF_M_GRD.nc"
sno_nc_file_path = "./raw/MESH-Scripts/Model_Workflow/vector_based_workflow/6_model_runs/results/SNO_M_GRD.nc"
output_db_path = "./out/mesh.gwfvisdb"

# %% read input files
shape_reader = shapefile.Reader(shape_file_path)
rff = nc.Dataset(rff_nc_file_path)
sno = nc.Dataset(sno_nc_file_path)

# %% dataset info
info = [gwfvis_db.Info(key="name", value="MESH Example", label="Name")]

# %% locations
locations: Sequence[gwfvis_db.Location] = [
    gwfvis_db.Location(
        id=shape_record.record["COMID"],
        geometry=shape_record.shape.__geo_interface__,
        metadata=dict(zip(metadata_fields, shape_record.record)),
    )
    for shape_record in shape_reader.iterShapeRecords()
]

# %% dimensions
time_dimension_size = rff.dimensions["time"].size
time_dimension = gwfvis_db.Dimension(id=0, name="time", size=time_dimension_size)
dimensions = [time_dimension]

# %% variables
rff_variable = gwfvis_db.Variable(
    id=0, name="RFF", dimensions=dimensions, unit="mm", description="Total runoff [mm]"
)
sno_variable = gwfvis_db.Variable(
    id=1,
    name="SNO",
    dimensions=dimensions,
    unit="mm",
    description="Liquid water content of the snow [mm]",
)
variables = [rff_variable, sno_variable]

# %% values
values: Sequence[gwfvis_db.Value] = []
for i, location in enumerate(sorted(locations, key=lambda l: l.metadata["COMID"])):
    for timestamp in range(time_dimension_size):
        values.append(
            gwfvis_db.Value(
                location=location,
                variable=rff_variable,
                value=float(rff.variables["RFF"][timestamp][0][i]),
                dimension_dict={time_dimension: timestamp},
            )
        )
        values.append(
            gwfvis_db.Value(
                location=location,
                variable=sno_variable,
                value=float(sno.variables["SNO"][timestamp][0][i]),
                dimension_dict={time_dimension: timestamp},
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
