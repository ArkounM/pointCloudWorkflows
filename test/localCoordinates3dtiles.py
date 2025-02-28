import os
import subprocess
import time
import json

# Specify directories
lazDirectory = r"E:/_PointCloud/Workflow_2/LAZ/"
tileDirectory = r"E:/_PointCloud/Workflow_4/NoSRS/"

# For output tile directory, if does not exist make directory
if not os.path.exists(tileDirectory):
    os.makedirs(tileDirectory)

print("Beginning first step of the pipeline to convert LAZ file to 3D tile")

# For each .laz file in lazDirectory begin py3dtile conversion pipeline
for file in os.listdir(lazDirectory):
    if file.endswith(".laz"):
        inputFile = os.path.join(lazDirectory, file)
        outputFolder = os.path.join(tileDirectory, file.split(".")[0])
        
        # Create output folder for each .laz file
        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)

        #Measure the start time
        start_time = time.time()
        
        # Run py3dtiles convert process. the --cache_size controls the memory allocated to the task
        # The default value is 1/10 of the RAM, but you can increase it if you have enough memory available
        # Tests show that 32000 MB is a good value for a 64 GB RAM machine and ensures the process runs smoothly
        # Cache size can be adjusted based on the available memory on your machine
        subprocess.run(["py3dtiles", "convert", inputFile, "--out", outputFolder, "--cache_size", "32000", "--overwrite"])

        #Measure the end time
        end_time = time.time()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time

        # Print a message indicating the process is complete for the current file
        print(f"Completed processing {inputFile} in {elapsed_time:.2f} seconds")

# Print a message indicating the process is complete for all files
print("All files turned into 3D tiles successfully")


print("Now beginning conversion of .json file to apply world transformations")
# Define the new transform values (first 12 values to replace) 
# These values adjust the rotation of model to be perpendicular to the ground and oriented north
new_transform_first_12 = [
    0.9690322530945821, 0.2469341865000208, 0.0, 0.0,
    -0.17587543683299575, 0.6901797326400464, 0.7019400026866237, 0.0,
    0.17333298353524487, -0.6802025023406401, 0.7122360792800965, 0.0
]

# Values to add to the last four values
values_to_add = [-83930.27, 1920130.78, 4519205.92, 0.0]  # Keep last value unchanged

# Modify the transform values in each tileset.json file
for folder in os.listdir(tileDirectory):
    folder_path = os.path.join(tileDirectory, folder)
    tileset_path = os.path.join(folder_path, "tileset.json")

    if os.path.exists(tileset_path):  # Ensure tileset.json exists in the folder
        with open(tileset_path, "r") as file:
            data = json.load(file)

        # Modify the "transform" key
        if "root" in data and "transform" in data["root"]:
            transform = data["root"]["transform"]

            # Replace the first 12 values
            transform[:12] = new_transform_first_12

            # Add to the last four values
            transform[-4:] = [transform[i] + values_to_add[i - 12] for i in range(12, 16)]

            # Save the updated transform back
            data["root"]["transform"] = transform

            with open(tileset_path, "w") as file:
                json.dump(data, file, indent=4)

            print(f"Modified tileset.json in {folder_path}")

print("All tileset.json files updated successfully.")

from osgeo import osr

# Define source (EPSG:2951 - NAD83(CSRS) / UTM zone 19N)
source_srs = osr.SpatialReference()
source_srs.ImportFromEPSG(2951)

# Define target (EPSG:4978 - WGS 84 Geocentric)
target_srs = osr.SpatialReference()
target_srs.ImportFromEPSG(4978)

# Create transformation
transform = osr.CoordinateTransformation(source_srs, target_srs)

# Input coordinates (Easting, Northing, Elevation)
easting, northing, elevation = 367112.6840, 5031109.4180, 77.572

# Convert to Geocentric (X, Y, Z)
x, y, z = transform.TransformPoint(easting, northing, elevation)

print(f"Geocentric Coordinates (EPSG:4978):\nX = {x:.3f}, Y = {y:.3f}, Z = {z:.3f}")
