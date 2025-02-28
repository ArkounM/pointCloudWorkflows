import os
import json
from osgeo import osr

tileDirectory = r"E:/_PointCloud/Workflow_3/NoSRS/"

print("Now beginning conversion of .json file to apply world transformations")

# Define new transform values
new_transform_first_12 = [
    0.9690322530945821, 0.2469341865000208, 0.0, 0.0,
    -0.17587543683299575, 0.6901797326400464, 0.7019400026866237, 0.0,
    0.17333298353524487, -0.6802025023406401, 0.7122360792800965, 0.0
]

# Define offset values
offsets = [367112.6840, 5031109.4180, 77.572, 1.0]

# Initialize coordinate transformation
source_srs = osr.SpatialReference()
source_srs.ImportFromEPSG(2951)

target_srs = osr.SpatialReference()
target_srs.ImportFromEPSG(4978)

transform_coords = osr.CoordinateTransformation(source_srs, target_srs)

# Process tileset.json in each folder
for folder in os.listdir(tileDirectory):
    folder_path = os.path.join(tileDirectory, folder)
    tileset_path = os.path.join(folder_path, "tileset.json")

    if os.path.exists(tileset_path):
        with open(tileset_path, "r") as file:
            data = json.load(file)

        if "root" in data and "transform" in data["root"]:
            transform = data["root"]["transform"]
            
            # Replace first 12 values
            transform[:12] = new_transform_first_12
            
            # Extract x, y, z and apply offsets
            x, y, z, _ = transform[-4:]
            x += offsets[0]
            y += offsets[1]
            z += offsets[2]
            
            # Convert to EPSG:4978
            x_new, y_new, z_new = transform_coords.TransformPoint(x, y, z)
            
            # Update transform
            transform[-4:] = [x_new, y_new, z_new, 1.0]
            data["root"]["transform"] = transform

            with open(tileset_path, "w") as file:
                json.dump(data, file, indent=4)

            print(f"Updated tileset.json in {folder_path}")

print("All tileset.json files updated successfully.")