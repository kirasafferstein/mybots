import pybullet as p
import time
import pybullet_data #Tell pybullet where to find .urdf

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())


# Insert forces (gravity)
p.setGravity(0,0,-9.8)

# Add a floor for the box to collide with
planeId = p.loadURDF("plane.urdf")


# Read in the world described in box.sdf
p.loadSDF("boxes.sdf")


# Slow things down to see simulated world 
for i in range(1000):
	p.stepSimulation()

	# Sleep the code by 1/60th of a second during each pass
	time.sleep(1/60)	
	
	# Print value of for loop
	print(f"Iteration number: {i}")	

p.disconnect()
