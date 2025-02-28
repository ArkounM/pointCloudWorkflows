import json

# Define the new transform values (first 12 values to replace) 
# These values adjust the rotation of model to be perpendicular to the ground and oriented north
new_transform_first_12 = [
    0.9690322530945821, 0.2469341865000208, 0.0, 0.0,
    -0.17587543683299575, 0.6901797326400464, 0.7019400026866237, 0.0,
    0.17333298353524487, -0.6802025023406401, 0.7122360792800965, 0.0
]

# Values to add to the last four values
values_to_add = [-83930.27, 1920130.78, 4519205.92, 0.0]  # Keep last value unchanged

# Load the JSON file
file_path = "E:/_PointCloud/Workflow_3/tileset.json"

with open(file_path, "r") as file:
    data = json.load(file)

# Modify the "transform" key in the root
if "root" in data and "transform" in data["root"]:
    transform = data["root"]["transform"]

    # Replace the first 12 values
    transform[:12] = new_transform_first_12

    # Add to the last four values
    transform[-4:] = [transform[i] + values_to_add[i - 12] for i in range(12, 16)]

    # Save the updated transform back
    data["root"]["transform"] = transform

# Save the modified JSON back to a file
output_path = "E:/_PointCloud/Workflow_3/tileset_Added.json"
with open(output_path, "w") as file:
    json.dump(data, file, indent=4)

print(f"Modified tileset saved to {output_path}")
