import pyrosim.pyrosim as pyrosim
import random

def Create_World():	

	# Tell pyrosim name of the file where information should be stored
	pyrosim.Start_SDF("world.sdf")

	# Create a single block at the origin
	#pyrosim.Send_Cube(name="Box", pos=[0, -2, 0.5], size=[1, 1, 1])

	# Create grid of blocks
	grid_rows = 10
	grid_cols = 10
	spacing = 7

	for row in range(grid_rows):
		for col in range(grid_cols):
			x = row * spacing + 4 # Start infront of robot
			y = (col - grid_cols // 2) * spacing + spacing / 2
			z = 0.5
			pyrosim.Send_Cube(name=f"Obstacle_{row}_{col}", pos=[x,y,z], size =[1,1,1])

	pyrosim.End()

def Generate_Body():
	pyrosim.Start_URDF("body.urdf")
	
	# Create torso
	pyrosim.Send_Cube(name="Torso", pos=[1.5, 0.0, 1.5], size=[1,1,1])
	
	# Create joints to connect torso and BackLeg
	pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg", type = "revolute", position = [1.0,0,1.0], jointAxis= "1 0 0")

	# Create Backleg
	pyrosim.Send_Cube(name="BackLeg", pos=[-0.5, 0.0, -0.5], size=[1,1,1])

    # Create joints to connect Torso and FrontLeg
	pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg", type = "revolute", position = [2.0,0,1.0], jointAxis= "1 0 0")

    # Create frontleg
	pyrosim.Send_Cube(name="FrontLeg", pos=[0.5, 0.0, -0.5], size=[1,1,1])

	pyrosim.End()

def Generate_Brain():
    pyrosim.Start_NeuralNetwork("brain.nndf")

    # Define sensor neurons
    pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
    pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
    pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")

    # Define motor neurons
    pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
    pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")

    # Connect them with synapses
    sensor_neuron_ids = [0, 1, 2]
    motor_neuron_ids = [3, 4]

    for sensor in sensor_neuron_ids:
        for motor in motor_neuron_ids:
            weight = random.uniform(-1, 1)
            pyrosim.Send_Synapse(sourceNeuronName=sensor, targetNeuronName=motor, weight=weight)

    pyrosim.End()  # This must come AFTER all the Send_* calls

Create_World()
Generate_Body()
Generate_Brain()

