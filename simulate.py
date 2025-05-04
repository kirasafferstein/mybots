import sys
from simulation import SIMULATION

#print(f"Starting simulate.py with ID {sys.argv[2]}")

# Get mode (DIRECT or GUI)
if len(sys.argv) > 1:
    directOrGUI = sys.argv[1]
else:
    directOrGUI = "GUI"

# Get solution ID
if len(sys.argv) > 2:
    solutionID = sys.argv[2]
else:
    solutionID = "0"
    
# Get body and world filenames
bodyFile = sys.argv[3] if len(sys.argv) > 3 else "body.urdf"
worldFile = sys.argv[4] if len(sys.argv) > 4 else "world.sdf"

# Get fitness type from CLI
fitnessType = sys.argv[5] if len(sys.argv) > 5 else "A"

# Pass all to the simulation
sim = SIMULATION(directOrGUI, solutionID, bodyFile, worldFile)
sim.Run()
sim.Get_Fitness()

# Pass both to simulation
#sim = SIMULATION(directOrGUI, solutionID)
#sim.Run()
#sim.Get_Fitness()


'''
import pybullet as p
import time
import pybullet_data #Tell pybullet where to find .urdf
import pyrosim.pyrosim as pyrosim
import numpy
import random
import constants as c

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Insert forces (gravity)
p.setGravity(0,0,c.GRAVITY)

# Add a floor for the box to collide with
planeId = p.loadURDF("plane.urdf")

# Simulate a world stored in world.sdf and a robot stored in body.urdf
robotId = p.loadURDF("body.urdf")

# Read in the world described in world.sdf
p.loadSDF("world.sdf")

# Pyrosim additional setting up to simulate sensors
# RobotId is an integer indicating which robot to prepare for simulation
# Future work: read in diff urdf files, store resulting integers in array, call this n times with each integer in the array (creates swarm of robots)
pyrosim.Prepare_To_Simulate(robotId)

# Generate sinusoidal motion
#t = numpy.linspace(0, 2 * numpy.pi, 1000)  # Time vector
#targetAngles = numpy.sin(t) * (numpy.pi / 4)  # Scale to [-π/4, π/4]

frontLegMotorCommands = numpy.zeros(c.SIMULATION_STEPS)
backLegMotorCommands = numpy.zeros(c.SIMULATION_STEPS)

# Construct motor command vector
#targetAngles = amplitude * numpy.sin(frequency * numpy.linspace(0, 2 * numpy.pi, 1000) + phaseOffset)
targetAngles = numpy.zeros(c.SIMULATION_STEPS)
for i in range(c.SIMULATION_STEPS):
	time_scaled = i / (c.SIMULATION_STEPS/c.backLegFrequency) # Normalized time step
	frontLegMotorCommands[i] = c.frontLegAmplitude * numpy.sin(2 * numpy.pi * time_scaled + c.frontLegPhaseOffset)
	backLegMotorCommands[i] = c.backLegAmplitude * numpy.sin(2 * numpy.pi * time_scaled + c.backLegPhaseOffset)

#numpy.save("data/frontLegMotorCommands.npy", frontLegMotorCommands)
#numpy.save("data/backLegMotorCommands.npy", backLegMotorCommands)
#exit()

# Saving sensor values in a vector:

# Create numpy vector filled with zeros
backLegSensorValues = numpy.zeros(c.SIMULATION_STEPS)
frontLegSensorValues = numpy.zeros(c.SIMULATION_STEPS)

# Slow things down to see simulated world 
for i in range(c.SIMULATION_STEPS):
	p.stepSimulation()

	# Add a touch sensor to the back leg and store in vector
	backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")

	# Add a touch sensor to the front leg
	frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

 	# Simulate a motor that supplies force to one of the joints
	pyrosim.Set_Motor_For_Joint(
	bodyIndex = robotId,
	jointName = b'Torso_BackLeg',
	controlMode = p.POSITION_CONTROL,
	#targetPosition = (random.random() * numpy.pi) - (numpy.pi / 2.0),
	targetPosition = backLegMotorCommands[i],
	maxForce = 25) #jumps

	pyrosim.Set_Motor_For_Joint(
	bodyIndex = robotId,
	jointName = b'Torso_FrontLeg',
	controlMode = p.POSITION_CONTROL,
	#targetPosition = (random.random() * numpy.pi) - (numpy.pi / 2.0),
	targetPosition = frontLegMotorCommands[i],
	maxForce = 25)


	# Sleep the code by 1/60th of a second during each pass
	time.sleep(c.TIME_STEP)	
	
	# Print value of for loop
	print(f"Iteration number: {i}")	

# Save backLegSensorValues to a file in data directory numpy.save("data/backLegSensorValues.npy", backLegSensorValues)
numpy.save("data/frontLegSensorValues.npy", frontLegSensorValues)
numpy.save("data/backLegSensorValues.npy", backLegSensorValues)

# Print vector of stored sensor values for backLegTouch
print("Back leg sensor values: ", backLegSensorValues)
print(frontLegSensorValues)

p.disconnect()

'''
