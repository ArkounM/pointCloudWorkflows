@echo off
setlocal enabledelayedexpansion

:: Set input and output directories
set "INPUT_DIR=E:\_PointCloud\Workflow_5\GLB\P28_01_Int_Lvl6__629C__20190308_A"
set "OUTPUT_DIR=E:\_PointCloud\Workflow_5\DRACO\P28_01_Int_Lvl6__629C__20190308_A"

:: Ensure output directory exists
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

:: Loop through all .glb files in the input directory
for %%f in ("%INPUT_DIR%\*.glb") do (
    echo Compressing %%~nf.glb...
    node gltf-pipeline.js -i "%%f" -o "%OUTPUT_DIR%\%%~nf.glb" --draco.compressMeshes --draco.compressionLevel=10 --draco.quantizePositionBits=14
)

echo Done!
pause
