import numpy
import os
import pyrosim.pyrosim as pyrosim
import random
import time

class SOLUTION:
    def __init__(self, myID):
        self.myID = myID
        self.weights = numpy.random.rand(3, 2)
        self.weights = self.weights * 2 - 1  # Scale to [-1, +1]

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()

        print(f"Launching simulate.py for solution {self.myID}")
        os.system(f"start /B py simulate.py {directOrGUI} {self.myID}")

    def Wait_For_Simulation_To_End(self):
        fitnessFileName = f"fitness{self.myID}.txt"
    
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)

        with open(fitnessFileName, "r") as fitnessFile:
            self.fitness = float(fitnessFile.read())

        os.remove(fitnessFileName)

    def Set_ID(self, newID):
        self.myID = newID

    def Mutate(self):
        randomRow = random.randint(0, 2)
        randomColumn = random.randint(0, 1)
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
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[0, -2, 0.5], size=[1, 1, 1])
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[1.5, 0.0, 1.5], size=[1,1,1])
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[1.0,0,1.0])
        pyrosim.Send_Cube(name="BackLeg", pos=[-0.5, 0.0, -0.5], size=[1,1,1])
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[2.0,0,1.0])
        pyrosim.Send_Cube(name="FrontLeg", pos=[0.5, 0.0, -0.5], size=[1,1,1])
        pyrosim.End()

    def Create_Brain(self):
        print(f"Creating brain{self.myID}.nndf with weights:\n{self.weights}")
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")

        pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")

        for currentRow in range(3):
            for currentColumn in range(2):
                weight = self.weights[currentRow][currentColumn]
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn+3, weight=weight)

        pyrosim.End()