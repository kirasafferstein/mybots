import pybullet as p
import time

physicsClient = p.connect(p.GUI)

# Read in the world described in box.sdf
p.loadSDF("box.sdf")


# Slow things down to see simulated world 
for i in range(1000):
	p.stepSimulation()

	# Sleep the code by 1/60th of a second during each pass
	time.sleep(1/60)	
	
	# Print value of for loop
	print(f"Iteration number: {i}")	

p.disconnect()
