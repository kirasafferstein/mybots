import pyrosim.pyrosim as pyrosim
import pyrosim.pyrosim as pyrosim

# Tell pyrosim name of the file where information should be stored
pyrosim.Start_SDF("boxes.sdf")

# Set initial block dimensions
base_length = 1
base_width = 1
base_height = 1

# Initial position for the first tower's base
base_x = 0
base_y = 0
base_z = base_height / 2  # Bottom of the block on the floor

# Create 25 towers using 3 nested loops
for row in range(5):  # 5 rows
    for col in range(5):  # 5 columns
        # Set the base position for the current tower
        x = base_x + col * base_length 
        y = base_y + row * base_width 
        z = base_z  # Starting height of the tower

        # Reset block dimensions for the current tower
        length = base_length
        width = base_width
        height = base_height

        # Create a tower with 10 blocks
        for i in range(10):
            # Send the current block in the tower
            pyrosim.Send_Cube(
                name=f"Box_{row}_{col}_{i + 1}",
                pos=[x, y, z],
                size=[length, width, height],
            )

            # Modify position for the next block (directly on top of the current block)
            z += height  # Move the block up by its height

            # Reduce size for the next block (90% of the current size)
            length *= 0.9
            width *= 0.9
            height *= 0.9

pyrosim.End()



