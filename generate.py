import pyrosim.pyrosim as pyrosim

def Create_World():	

	# Tell pyrosim name of the file where information should be stored
	pyrosim.Start_SDF("world.sdf")

	# Create a single block at the origin
	pyrosim.Send_Cube(name="Box", pos=[0, -2, 0.5], size=[1, 1, 1])

	pyrosim.End()

def Generate_Body():
	pyrosim.Start_URDF("body.urdf")
	
	# Create torso
	pyrosim.Send_Cube(name="Torso", pos=[1.5, 0.0, 1.5], size=[1,1,1])
	
	# Create joints to connect torso and BackLeg
	pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg", type = "revolute", position = [1.0,0,1.0])

	# Create Backleg
	pyrosim.Send_Cube(name="BackLeg", pos=[-0.5, 0.0, -0.5], size=[1,1,1])

    # Create joints to connect Torso and FrontLeg
	pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg", type = "revolute", position = [2.0,0,1.0])

    # Create frontleg
	pyrosim.Send_Cube(name="FrontLeg", pos=[0.5, 0.0, -0.5], size=[1,1,1])

	pyrosim.End()

def Generate_Brain():
	pyrosim.Start_NeuralNetwork("brain.nndf")

	# Sensor nuerons receive values from sensors
	pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
	pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
	pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")

	pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")
	pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")

	#pyrosim.Send_Synapse( sourceNeuronName = 1 , targetNeuronName = 3 , weight = 1.5 )
	#pyrosim.Send_Synapse( sourceNeuronName = 2 , targetNeuronName = 3 , weight = 1.5 )

	# Testing different combinations and weights
	pyrosim.Send_Synapse( sourceNeuronName = 1 , targetNeuronName = 3 , weight = 0.5 )
	pyrosim.Send_Synapse( sourceNeuronName = 2 , targetNeuronName = 4 , weight = 1.5 )


	pyrosim.End()

Create_World()
Generate_Body()
Generate_Brain()

