# pointCloudWorkflows
Workflows for prepping Point Cloud models to 3D tiles for use in Unreal Engine 5 (UE5)

# Overview
This project holds python script meant to process and manipulate Point Clouds specifically for UE5. The main script (E57_3DTiles.py) batch converts a folder of e57 files into 3d tiles compatible with the Cesium Unreal Engine plugin. The script will also reproject the e57 files to the correct coordinate system.

Future plans for this repo include meshTo3Dtiles and pointcloudToMesh workflows


# Requirements
IMPORTANT! This script is intended to be run in a Conda environment. Create a new Conda environment to download
the following packages:

PDAL 2.8.0 (https://pdal.io/)
py3dtiles (https://py3dtiles.org/v8.0.2/cli.html#convert)
3D Tiles Tools (https://github.com/CesiumGS/3d-tiles-tools)

Below is the step by step breakdown to download the required packages in a Conda environment:

Create a new Conda environment, open terminal and install PDAL:

    conda install -c conda-forge pdal=2.8.0

Next install py3dtiles + laz reading packages

    pip install py3dtiles
    pip install py3dtiles[las]
    pip install laspy[laszip]

To install 3d-tiles-tools. You will need nodejs in this env to do so

    conda install -c conda-forge nodejs

If nodejs gives errors try the following

    conda install conda-forge/label/cf201901::nodejs
    conda update nodejs

Finally install 3d-tiles-tools

    npm install 3d-tiles-tools

You shouldnow have all the packages. In the shell, navigate to the directory where you have cloned this repo and run the script:

    py E57_3DTiles.py

# Tools
E57_3DTiles.py 

Prior to use of this script, the user will need to set the input e57Directory, and the output LAZDirectory, tileDirectory and gzip directory. By default, the script assumes that you will want to keep the files at each step of the workflow but the user may set LAZ and tile Directories to be temp folders that will be deleted once the pipeline is complete. 

The script assumes that your files are E57 files use the EPSG:2951 coordinate system, which by default are not compatible with the Cesium Unreal Engine plugin. The script will reproject the E57 files to the Cesium compatible EPSG:4978 coordinate system. Export them as .laz files, then convert them to 3D tiles and finally GZIP the 3D tiles to reduce final file size.