import json

def update_transform_in_tileset(input_file):
    transform_matrix = [
        0.9690322530945821, 0.2469341865000208, 0.0, 0.0,
       -0.17587543683299575, 0.6901797326400464, 0.7019400026866237, 0.0,
        0.17333298353524487, -0.6802025023406401, 0.7122360792800965, 0.0,
        1107436.97, -4345862.99, 4520064.87, 1.0
    ]
    
    # Read the original tileset.json file
    with open(input_file, 'r') as file:
        data = json.load(file)
    
    # Update the transform matrix in the root if it exists
    if "root" in data:
        data["root"]["transform"] = transform_matrix
    
    # Write the modified data back to the same file
    with open(input_file, 'w') as file:
        json.dump(data, file, indent=4)
    
    print(f"Updated transform matrix in {input_file}")

# Example usage
input_file = "E:/_PointCloud/Workflow_7/LAStools/TILE/P28_01_Int_Lvl6__629C__20190308_A/tileset.json"
update_transform_in_tileset(input_file)
