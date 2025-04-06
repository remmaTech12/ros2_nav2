import numpy as np
from PIL import Image
import trimesh
from trimesh.creation import box
from trimesh.scene import Scene

# Parameters
input_file = "maze.pgm"
output_file = "maze.stl"
resolution = 0.05
wall_height = 1.0

# Load image
image = Image.open(input_file).convert("L")
image = np.array(image, dtype=np.uint8)
height, width = image.shape

scene = Scene()

# Threshold for black (wall)
black_threshold = 128

for y in range(height):
    for x in range(width):
        if image[y, x] < black_threshold:
            px = (x - width / 2) * resolution
            py = (height / 2 - y) * resolution
            pz = wall_height / 2

            wall = box(extents=[resolution, resolution, wall_height])
            wall.apply_translation([px, py, pz])
            scene.add_geometry(wall)

scene.export(output_file)
print(output_file + " created!")
