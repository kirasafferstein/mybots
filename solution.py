import numpy
import os
import pyrosim.pyrosim as pyrosim
import random
import time
import constants as c

class SOLUTION:
    def __init__(self, myID):
        self.myID = myID
        self.weights = numpy.random.rand(c.numSensorNeurons, c.numMotorNeurons)
        self.weights = self.weights * 2 - 1  # Scale to [-1, +1]

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()

        #print(f"Launching simulate.py for solution {self.myID}")
        os.system(f"start /B py simulate.py {directOrGUI} {self.myID} {self.bodyFileName} {self.worldFileName}")


    def Wait_For_Simulation_To_End(self):
        fitnessFileName = f"fitness{self.myID}.txt"
 
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)

        # Retry reading if the file is still in use (locked by another process)
        while True:
            try:
                with open(fitnessFileName, "r") as fitnessFile:
                    self.fitness = float(fitnessFile.read())
                os.remove(fitnessFileName)
                break  # Successfully read and deleted the file
            except PermissionError:
                print(f"Waiting for {fitnessFileName} to be unlocked...")
                time.sleep(0.1)  # Wait before trying again

    def Set_ID(self, newID):
        self.myID = newID

    def Mutate(self):
        randomRow = random.randint(0, c.numSensorNeurons - 1)  # Choose a random sensor neuron
        randomColumn = random.randint(0, c.numMotorNeurons - 1)  # Choose a random motor neuron
        self.weights[randomRow, randomColumn] = random.random() * 2 - 1

    def Get_Fitness(self):
        fitnessFileName = f"fitness{self.myID}.txt"

        # Wait until the fitness file exists
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)

        # Once the file is found, read it
        with open(fitnessFileName, "r") as fitnessFile:
            self.fitness = float(fitnessFile.read())
        
        print(f"Fitness for solution {self.myID}: {self.fitness}")

        # Clean up the fitness file
        os.system(f"del {fitnessFileName}")
        return self.fitness

    def Create_World(self):
        self.worldFileName = f"world{self.myID}.sdf"
        pyrosim.Start_SDF(self.worldFileName)

        # Generate a grid of blocks
        grid_rows = 3
        grid_cols = 5
        spacing = 5

        for row in range(grid_rows):
            for col in range(grid_cols):
                x_offset = -row * spacing - 4  # Still moving toward -X
                y_offset = (col - grid_cols // 2) * spacing

                if row % 2 == 1:
                    y_offset += spacing / 2  # Offset odd rows to break symmetry
                z = 0.5  # So it sits on the ground
                pyrosim.Send_Cube(name=f"Obstacle_{row}_{col}", pos=[x_offset, y_offset, z], size=[1, 1, 1])

        pyrosim.End()

    def Create_Body(self):        
        self.bodyFileName = f"body{self.myID}.urdf"
        pyrosim.Start_URDF(self.bodyFileName)

        # Torso
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.0], size=[1, 1, 1])

        # --- BACK LEG ---
        pyrosim.Send_Joint("Torso_BackLeg", "Torso", "BackLeg", "revolute", [0, -0.5, 1.0], jointAxis="1 0 0", lowerLimit="-0.6", upperLimit="0.6")
        pyrosim.Send_Cube("BackLeg", pos=[0, -0.5, 0], size=[0.2, 1.0, 0.2])
        pyrosim.Send_Joint("BackLeg_BackLowerLeg", "BackLeg", "BackLowerLeg", "revolute", [0, -1.0, 0], jointAxis="1 0 0", lowerLimit="-0.6", upperLimit="0.6")
        pyrosim.Send_Cube("BackLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1.0])

        # --- FRONT LEG ---
        pyrosim.Send_Joint("Torso_FrontLeg", "Torso", "FrontLeg", "revolute", [0, 0.5, 1.0], jointAxis="1 0 0", lowerLimit="-0.6", upperLimit="0.6")
        pyrosim.Send_Cube("FrontLeg", pos=[0, 0.5, 0], size=[0.2, 1.0, 0.2])
        pyrosim.Send_Joint("FrontLeg_FrontLowerLeg", "FrontLeg", "FrontLowerLeg", "revolute", [0, 1.0, 0], jointAxis="1 0 0", lowerLimit="-0.6", upperLimit="0.6")
        pyrosim.Send_Cube("FrontLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1.0])

        # --- LEFT LEG ---
        pyrosim.Send_Joint("Torso_LeftLeg", "Torso", "LeftLeg", "revolute", [-0.5, 0, 1.0], jointAxis="0 1 0", lowerLimit="-0.6", upperLimit="0.6")
        pyrosim.Send_Cube("LeftLeg", pos=[-0.5, 0, 0], size=[1.0, 0.2, 0.2])
        pyrosim.Send_Joint("LeftLeg_LeftLowerLeg", "LeftLeg", "LeftLowerLeg", "revolute", [-1.0, 0, 0], jointAxis="0 1 0", lowerLimit="-0.6", upperLimit="0.6")
        pyrosim.Send_Cube("LeftLowerLeg", pos=[0, 0, -.5], size=[0.2, 0.2, 1.0])

        # --- RIGHT LEG ---
        pyrosim.Send_Joint("Torso_RightLeg", "Torso", "RightLeg", "revolute", [0.5, 0, 1.0], jointAxis="0 1 0", lowerLimit="-0.6", upperLimit="0.6")
        pyrosim.Send_Cube("RightLeg", pos=[0.5, 0, 0], size=[1.0, 0.2, 0.2])
        pyrosim.Send_Joint("RightLeg_RightLowerLeg", "RightLeg", "RightLowerLeg", "revolute", [1.0, 0, 0], jointAxis="0 1 0", lowerLimit="-0.6", upperLimit="0.6")
        pyrosim.Send_Cube("RightLowerLeg", pos=[0, 0, -.5], size=[0.2, 0.2, 1.0])
        pyrosim.End()

    def Create_Brain(self):
        #print(f"Current working directory: {os.getcwd()}")


        file_name = f"brain{self.myID}.nndf"
        #print(f"Creating {file_name} with weights:\n{self.weights}")
        
        # Absolute path or check the current working directory
        file_path = os.path.join(os.getcwd(), file_name)
        #print(f"Saving brain file at: {file_path}")


        pyrosim.Start_NeuralNetwork(file_path)

        # Sensor neurons for all body parts
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
        pyrosim.Send_Sensor_Neuron(name=3, linkName="LeftLeg")
        pyrosim.Send_Sensor_Neuron(name=4, linkName="RightLeg")
        pyrosim.Send_Sensor_Neuron(name=5, linkName="FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=6, linkName="BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=7, linkName="LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=8, linkName="RightLowerLeg")

        # Motor neurons for all joints
        pyrosim.Send_Motor_Neuron(name=9, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=10, jointName="Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name=11, jointName="Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name=12, jointName="Torso_RightLeg")
        pyrosim.Send_Motor_Neuron(name=13, jointName="FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron(name=14, jointName="BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron(name=15, jointName="LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron(name=16, jointName="RightLeg_RightLowerLeg")

        # Create synapses based on the weights of the neural network
        for currentRow in range(c.numSensorNeurons):  # sensor neurons
            for currentColumn in range(c.numMotorNeurons):  # motor neurons
                weight = self.weights[currentRow][currentColumn]
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn + c.numSensorNeurons, weight=weight)


        pyrosim.End()

        # Check if the brain file has been created
        if os.path.exists(f"brain{self.myID}.nndf"):
            print(f"brain{self.myID}.nndf file created successfully!")
        else:
            print(f"Error: brain{self.myID}.nndf file not created!")
            exit()
        
