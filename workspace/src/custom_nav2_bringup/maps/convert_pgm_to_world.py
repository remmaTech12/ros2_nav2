import numpy as np
from PIL import Image

input_file  = "maze.pgm"
output_file = "maze.world"
image = Image.open(input_file).convert("L")
image = np.array(image, dtype=np.uint8)

resolution = 0.05  # [m/px]: x [m/px] means x meter for 1 px.
height, width = image.shape

# Header part of .world file
world_template_list = ["""<?xml version="1.0" ?>
<sdf version="1.6">
  <world name="maze">
    <include>
      <uri>model://ground_plane</uri>
    </include>
    <include>
      <uri>model://sun</uri>
    </include>

    <gui fullscreen='0'>
      <camera name='user_camera'>
        <pose frame=''>0 0 10 0 1.570796 0</pose>
        <view_controller>orbit</view_controller>
        <projection_type>perspective</projection_type>
      </camera>
    </gui>
"""]

wall_height = 1.0

# Convert a consecutive lateral line to a wall
for y in range(height):
    x = 0
    while x < width:
        black_threshold = 128
        if image[y, x] < black_threshold:  # Judge black parts
            start_x = x
            # Search for consecutive black parts
            while x < width and image[y, x] < black_threshold: 
                x += 1
            end_x = x

            wall_x = ((start_x + end_x - 1) / 2 - width / 2) * resolution
            wall_y = (height / 2 - y) * resolution
            wall_length = (end_x - start_x) * resolution
            world_template_list.append(f"""
    <model name="wall_{start_x}_{y}">
      <static>true</static>
      <pose>{wall_x} {wall_y} {wall_height/2} 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>{wall_length} {resolution} {wall_height}</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>{wall_length} {resolution} {wall_height}</size>
            </box>
          </geometry>
        </visual>
      </link>
    </model>
""")
        x += 1

# Footer part of .world file
world_template_list.append("""
  </world>
</sdf>
""")

# Save as .world file
with open("../worlds/" + output_file, "w") as f:
    f.write("".join(world_template_list))

print(output_file + " has been created!!")
