import os
import subprocess
import json

def run_command(command):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(result.stdout)

def convert_e57_to_laz(e57_input_folder, laz_output_folder):
    for file in os.listdir(e57_input_folder):
        if file.endswith(".e57"):
            inputFile = os.path.join(e57_input_folder, file)
            outputFolder = os.path.join(laz_output_folder, f"{os.path.splitext(file)[0]}.laz")
            command = f"C:/Users/arkoun.merchant/Documents/LAStools/bin/e572las -v -i {inputFile} -o {outputFolder}"
            run_command(command)

def build_entwine(input_folder, output_folder):
    for file in os.listdir(input_folder):
        if file.endswith(".laz"):
            laz_file = os.path.join(input_folder, file)
            entwine_folder = os.path.join(output_folder, os.path.splitext(file)[0])
            command = f"entwine build -i {laz_file} -o {entwine_folder} -f"
            run_command(command)

def convert_entwine_to_tiles(ept_folder, tile_folder):
    command = f"entwine convert -i {ept_folder} -o {tile_folder} --truncate -g 16"
    run_command(command)

def update_tileset_json(tile_folder):
    transform_matrix = [
        0.9690322530945821, 0.2469341865000208, 0.0, 0.0,
       -0.17587543683299575, 0.6901797326400464, 0.7019400026866237, 0.0,
        0.17333298353524487, -0.6802025023406401, 0.7122360792800965, 0.0,
        1107436.97, -4345862.99, 4520064.87, 1.0
    ]
    
    for root, _, files in os.walk(tile_folder):
        if "tileset.json" in files:
            tileset_path = os.path.join(root, "tileset.json")
            with open(tileset_path, 'r') as file:
                data = json.load(file)
            
            if "root" in data:
                data["root"]["transform"] = transform_matrix
            
            with open(tileset_path, 'w') as file:
                json.dump(data, file, indent=4)
            print(f"Updated transform in {tileset_path}")

def gzip_tiles(tile_folder, gzip_folder):
    command = f"npx 3d-tiles-tools gzip -i {tile_folder} -o {gzip_folder}"
    run_command(command)

if __name__ == "__main__":
    e57_input_folder = "E:/_PointCloud/E57"
    laz_output_folder = "E:/_PointCloud/Workflow_9/LAZ"
    ept_output_folder = "E:/_PointCloud/Workflow_9/EPT"
    tile_output_folder = "E:/_PointCloud/Workflow_9/Tiles"
    gzip_output_folder = "E:/_PointCloud/Workflow_9/GZIP"

    if not os.path.exists(laz_output_folder):
         os.makedirs(laz_output_folder)
    if not os.path.exists(ept_output_folder):
        os.makedirs(ept_output_folder)
    if not os.path.exists(tile_output_folder):
        os.makedirs(tile_output_folder)
    if not os.path.exists(gzip_output_folder):
        os.makedirs(gzip_output_folder)
   
    convert_e57_to_laz(e57_input_folder, laz_output_folder)
    build_entwine(laz_output_folder, ept_output_folder)
    
    for ept_folder in os.listdir(ept_output_folder):
        ept_path = os.path.join(ept_output_folder, ept_folder)
        tile_path = os.path.join(tile_output_folder, ept_folder)
        convert_entwine_to_tiles(ept_path, tile_path)
        update_tileset_json(tile_path)
        gzip_tiles(tile_path, os.path.join(gzip_output_folder, ept_folder))


print("Removing tmp EPT and Unzipped Tile Folders")
os.rmdir(ept_output_folder)
os.rmdir(tile_output_folder)
print("Processing complete!")