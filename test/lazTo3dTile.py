import os
import subprocess
import time
import json
from osgeo import osr

# Specify directories
lazDirectory = r"E:/_PointCloud/Workflow_9/LAZ/"
tileDirectory = r"E:/_PointCloud/Workflow_10/TILE/"

# Create output tile directory if it does not exist
if not os.path.exists(tileDirectory):
    os.makedirs(tileDirectory)

print("Beginning first step of the pipeline to convert LAZ file to 3D tile")

# Process each .laz file
for file in os.listdir(lazDirectory):
    if file.endswith(".laz"):
        inputFile = os.path.join(lazDirectory, file)
        outputFolder = os.path.join(tileDirectory, file.split(".")[0])
        
        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)

        start_time = time.time()
        
        subprocess.run(["py3dtiles", "convert", inputFile, "--out", outputFolder, "--cache_size", "32000", "--overwrite"])

        elapsed_time = time.time() - start_time
        print(f"Completed processing {inputFile} in {elapsed_time:.2f} seconds")

print("All files turned into 3D tiles successfully")

print("Now beginning conversion of .json file to apply world transformations")

# Define new transform values
new_transform_first_12 = [
    0.9690322530945821, 0.2469341865000208, 0.0, 0.0,
    -0.17587543683299575, 0.6901797326400464, 0.7019400026866237, 0.0,
    0.17333298353524487, -0.6802025023406401, 0.7122360792800965, 0.0
]

# Define offset values. original values from revit survey point: [367112.6840, 5031109.4180, 77.572, 1.0]
# The below offsets are adjusted for UE5 tolerance X= -9.12m Y= -0.72m
offsets = [367103.5640, 5031108.6980, 77.5720, 1.0]

# Initialize coordinate transformation
source_srs = osr.SpatialReference()
source_srs.ImportFromEPSG(2951)

target_srs = osr.SpatialReference()
target_srs.ImportFromEPSG(4978)

transform_coords = osr.CoordinateTransformation(source_srs, target_srs)

# Process tileset.json in each folder to move values from local EPSG 2951 coordinates to global then convert to EPSG 4978
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

# Print a message indicating the process is complete for all files
print("All files turned into 3D tiles successfully")

'''Pipeline 3: GZIP the 3D tiles to reduce file size'''
# Set input and output directories. GZIP directory will need to be set by user 
gzipDirectory = r"E:/_PointCloud/Workflow_10/gzipDirectory"

# Ensure the output directory exists
if not os.path.exists(gzipDirectory):
    os.makedirs(gzipDirectory)

# Get all subdirectories in the input directory
folders = [f for f in os.listdir(tileDirectory) if os.path.isdir(os.path.join(tileDirectory, f))]

print("Starting 3D Tiles Gzip process...")

for folder in folders:
    inputFolder = os.path.join(tileDirectory, folder)
    outputFolder = os.path.join(gzipDirectory, folder)

    # Ensure output folder exists for each subdirectory
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    print(f"Processing: {inputFolder} -> {outputFolder}")

    # Run the 3D Tiles Tools Gzip command
    command = ["npx", "3d-tiles-tools", "gzip", "-i", inputFolder, "-o", outputFolder, "--force"]

    try:
        subprocess.run(command, check=True, shell=True)
        print(f"Finished processing: {inputFolder}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing {inputFolder}: {e}")

print("All folder are processed.")
# Print a message indicating the process is complete for all files
print("All processes are complete. 3D tiles are ready for use in Cesium or Unreal Engine!")