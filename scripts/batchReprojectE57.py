# This script is to batch convert a folder of e57 files into 3d tiles compatible with the Cesium
# Unreal Engine plugin. The script will also reproject the e57 files to the correct coordinate system.
# By default, the E57 files use the EPSG:2951 coordinate system, which is not compatible with the Cesiums
# Unreal Engine plugin. The script will reproject the E57 files to the Cesium compatible EPSG:4978 coordinate system
# Export them as .laz files and then convert them to 3D tiles.
'''
IMPORTANT! This script is intended to be run in a Conda environment. Create a new Conda environment to download
the following packages:
- PDAL 2.8.0 (https://pdal.io/)
- py3dtiles (https://py3dtiles.org/v8.0.2/cli.html#convert)
- 3D Tiles Tools (https://github.com/CesiumGS/3d-tiles-tools)

Below is the step by step breakdown to download the required packages in a Conda environment:

# Create a new Conda environment, open terminal:

$ conda install -c conda-forge pdal=2.8.0
$ pip install py3dtiles
    pip install py3dtiles[las]
    pip install laspy[laszip]
$ conda install -c conda-forge nodejs
    If nodejs gives errors try the following
        conda install conda-forge/label/cf201901::nodejs
        conda update nodejs
$ npm install 3d-tiles-tools

# You shouldnow have all the packages. Navigate to the database folder and run the script:
$ py batchReprojectE57.py
'''


# Import the required libraries
import os
import subprocess
import time

# Set the input and output directories. Both the LAZ and Tile directories can be temp directories if the user chooses
e57Directory = r"./e57Directory"
lazDirectory = r"./lazDirectory"
tileDirectory = r"./tileDirectory"


# Create the output laz and tile directory if it doesn't exist
if not os.path.exists(lazDirectory):
    os.makedirs(lazDirectory)
if not os.path.exists(tileDirectory):
    os.makedirs(tileDirectory)

'''Pipeline 1: Begin the process of converting the E57 files to LAZ files using PDAL 2.8.0'''
print("Beginnning the E57 to LAZ conversion process. This will translate the E57 files to world coordinates, reproject them to EPSG:4978 and export them as .laz files")

# Path to PDAL pipeline template
template_path = r"json/reprojectPipeline.json"

# Read the pipeline template
with open(template_path, 'r') as file:
    pipeline_template = file.read()

# Iterate over all .e57 files in the input directory
for filename in os.listdir(e57Directory):
    if filename.endswith(".e57"):
        input_file = os.path.join(e57Directory, filename)
        output_file = os.path.join(lazDirectory, f"{os.path.splitext(filename)[0]}.laz")

        # Print the current file being processed
        print(f"Processing {input_file}")

        # Replace placeholders with actual filenames
        pipeline = pipeline_template.replace("%%input_file%%", input_file).replace("%%output_file%%", output_file)

        # Write the modified pipeline to a temporary file
        temp_pipeline_path = "temp_pipeline.json"
        with open(temp_pipeline_path, 'w') as temp_file:
            temp_file.write(pipeline)

        # Measure the start time
        start_time = time.time()

        # Execute the PDAL pipeline. --nostream is enabled to ensure precision when translating the pointcloud location
        subprocess.run(["pdal", "pipeline", temp_pipeline_path, "--nostream"])

        # Measure the end time
        end_time = time.time()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time

        # Optionally, remove the temporary pipeline file
        os.remove(temp_pipeline_path)

        # Print a message indicating the process is complete for the current file
        print(f"Completed processing {input_file} in {elapsed_time:.2f} seconds")

# Print a message indicating the process is complete for all files
print("All files translated, reprojected and exported as .laz successfully")

'''Pipeline 2: Using py3dtiles to convert the LAZ files to 3D tiles'''

print("Now beginning the 3D tiles conversion process")

# Get list of .LAZ files in input directory
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
        subprocess.run(["py3dtiles", "convert", inputFile, "--out", outputFolder, "--cache_size", "32000"])

        #Measure the end time
        end_time = time.time()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time

        # Print a message indicating the process is complete for the current file
        print(f"Completed processing {inputFile} in {elapsed_time:.2f} seconds")

# Print a message indicating the process is complete for all files
print("All files turned into 3D tiles successfully")

'''Pipeline 3: GZIP the 3D tiles to reduce file size'''
# Set input and output directories
gzipDirectory = r"T:/HOK_Streamable-Assets/02_GENERATE/10_MODELS/POINTCLOUD/3Dtiles_GZIP"

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

