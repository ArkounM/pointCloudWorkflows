# pointCloudWorkflows
Workflows for prepping Point Cloud models to 3D tiles for use in Unreal Engine 5

# Overview
This script is to batch convert a folder of e57 files into 3d tiles compatible with the Cesium Unreal Engine plugin. The script will also reproject the e57 files to the correct coordinate system.

By default, the script assumes that your files are E57 files use the EPSG:2951 coordinate system, which by default are not compatible with the Cesium Unreal Engine plugin. The script will reproject the E57 files to the Cesium compatible EPSG:4978 coordinate system. Export them as .laz files, then convert them to 3D tiles and finally GZIP the 3D tiles to reduce final file size.
