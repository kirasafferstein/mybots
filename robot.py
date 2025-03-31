import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR
import constants as c
import numpy
import os
from pyrosim.neuralNetwork import NEURAL_NETWORK

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
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]
        xCoordinateOfLinkZero = basePosition[0]


        # Write to a temp file first
        tmpFile = f"tmp{self.solutionID}.txt"
        finalFile = f"fitness{self.solutionID}.txt"
        with open(tmpFile, "w") as f:
            f.write(str(xCoordinateOfLinkZero))

        # Rename to signal completion
        os.rename(tmpFile, finalFile)