import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR
import constants as c
import numpy
import os
from pyrosim.neuralNetwork import NEURAL_NETWORK
import time

class ROBOT:
    def __init__(self, solutionID, bodyFile):
        self.solutionID = solutionID
        self.robotId = p.loadURDF(bodyFile)
        pyrosim.Prepare_To_Simulate(self.robotId)

        self.nn = NEURAL_NETWORK(f"brain{solutionID}.nndf")

        self.Prepare_To_Sense()
        self.Prepare_To_Act()

        # Delete the brain file after loading
        # Clean up input files (optional but recommended)
        os.remove(f"brain{solutionID}.nndf")
        os.remove(bodyFile)  # ← This is the cleanup line

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName_bytes in pyrosim.jointNamesToIndices:
            jointName = jointName_bytes.decode("utf-8")
            self.motors[jointName] = MOTOR(jointName)

    def Sense(self, t):
        for sensor in self.sensors.values():
            sensor.Get_Value(t)

    def Think(self):
        self.nn.Update()

    def Act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motors[jointName].Set_Value(desiredAngle, self.robotId)

    def Save_Values(self):
        for linkName, sensor in self.sensors.items():
            numpy.save(f"data/{linkName}_sensorValues.npy", sensor.values)
        for jointName, motor in self.motors.items():
            numpy.save(f"data/{jointName}_motorValues.npy", motor.motorValues)

    def Get_Fitness(self):
        basePosition = p.getBasePositionAndOrientation(self.robotId)[0]
        x = basePosition[0]  # How far it made it through the grid

        time_elapsed = time.time() - self.start_time

        # Combined fitness: distance minus time penalty
        alpha = 0.05
        fitness = x - alpha * time_elapsed

        # Save to fitness file
        tmpFile = f"tmp{self.solutionID}.txt"
        finalFile = f"fitness{self.solutionID}.txt"
        with open(tmpFile, "w") as f:
            f.write(str(fitness))
        os.rename(tmpFile, finalFile)

        # Print useful info
        print(f"Robot {self.solutionID} → Distance: {x:.3f}, Time: {time_elapsed:.2f}s, Fitness: {fitness:.3f}")

        # Log all info for plotting
        with open("fitness_log.csv", "a") as log:
            log.write(f"{self.solutionID},{x},{time_elapsed},{fitness}\n")







