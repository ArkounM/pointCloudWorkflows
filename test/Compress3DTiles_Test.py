import os
import subprocess
import time

# Specify directories
lazDirectory = r"E:/_PointCloud/Workflow_2/LAZ/"
rotatedDirectory = r"E:/_PointCloud/Workflow_2/Rot/"
tileDirectory = r"E:/_PointCloud/Workflow_2/TILE/"

# If Directory doesn't exist, make directory
if not os.path.exists(rotatedDirectory):
    os.makedirs(rotatedDirectory)
if not os.path.exists(tileDirectory):
    os.makedirs(tileDirectory)

'''Pipeline 1: Begin the process of rotating LAZ file 45 degrees in the x-axis using PDAL 2.8.0'''
print("Begin the process of rotating LAZ file 45 degrees in the x-axis using PDAL 2.8.0")

# Path to PDAL pipeline template
template_path = r"E:/_GitRepos/pointCloudWorkflows/test/rotatePC.json"

# Read the pipeline template
with open(template_path, 'r') as file:
    pipeline_template = file.read()

# Iterate over all .lazfiles in the input directory
for filename in os.listdir(lazDirectory):
    if filename.endswith(".laz"):
        input_file = os.path.join(lazDirectory, filename)
        output_file = os.path.join(rotatedDirectory, f"{os.path.splitext(filename)[0]}.laz")

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
print("All files rotated and exported as .laz successfully")

'''Pipeline 2: Using py3dtiles to convert the LAZ files to 3D tiles'''

print("Now beginning the 3D tiles conversion process")

# Get list of .LAZ files in input directory
for file in os.listdir(rotatedDirectory):
    if file.endswith(".laz"):
        inputFile = os.path.join(rotatedDirectory, file)
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