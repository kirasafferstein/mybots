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
    def __init__(self, solutionID, bodyFile, fitnessType="A", cleanup=True):
        self.solutionID = solutionID
        self.fitnessType = fitnessType  # Set the fitness strategy (A or B)

        self.robotId = p.loadURDF(bodyFile)
        pyrosim.Prepare_To_Simulate(self.robotId)

        self.nn = NEURAL_NETWORK(f"brain{solutionID}.nndf")

        self.Prepare_To_Sense()
        self.Prepare_To_Act()

        self.collision_list = []
        self.distance_readings = []
        self.sensor_links_to_check = ['Torso', 'FrontLeg', 'BackLeg']  # Robot links

        # Delete the brain file after loading
        # os.remove(f"brain{solutionID}.nndf")
        # os.remove(bodyFile)  # Cleanup line
        if cleanup:
          os.remove(f"brain{solutionID}.nndf")
          os.remove(bodyFile)

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
        for linkName, sensor in self.sensors.items():
            sensor.Get_Value(t)
        self.Sense_Distance()

    def Track_Collisions(self):
        contact_points = p.getContactPoints(bodyA=self.robotId)
        for contact in contact_points:
            if contact[2] != self.robotId:  # only count if not self-self
                self.collision_list.append(contact)


    def Sense_Distance(self):
        for linkName in self.sensor_links_to_check:
            linkIndex = pyrosim.linkNamesToIndices.get(linkName, -1)
            if linkIndex == -1:
                continue  # Skip if missing

            linkState = p.getLinkState(self.robotId, linkIndex)
            linkPos = linkState[0]
            linkOri = linkState[1]
            matrix = p.getMatrixFromQuaternion(linkOri)
            forward_vector = [matrix[0], matrix[3], matrix[6]]

            # Raycast
            start = linkPos
            ray_length = 2
            end = [start[i] + ray_length * forward_vector[i] for i in range(3)]
            result = p.rayTest(start, end)[0]
            hitFraction = result[2]
            distance = hitFraction * ray_length

            self.distance_readings.append((linkName, distance))

            # Optionally overwrite sensor reading with distance
            #if linkName in self.sensors:
                #self.sensors[linkName].value = distance

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
        print(f"[DEBUG] Fitness Type: {self.fitnessType}")

        base_position = p.getBasePositionAndOrientation(self.robotId)[0]
        x = base_position[0]  # Forward progress
        y = base_position[1]  # Side movement
        time_elapsed = time.time() - self.start_time

        forward_progress = -x  # We want large X

        self.fitness = (
            5.0 * forward_progress
            - 0.1 * abs(y)
            - 0.005 * time_elapsed
            - 0.0002 * len(self.collision_list)
        )

        # Log fitness calculation
        print(f"[{self.fitnessType}] Fitness: {self.fitness:.3f} | x: {x:.2f}, y: {y:.2f}, time: {time_elapsed:.2f}, collisions: {len(self.collision_list)}")

        # Save fitness to file
        with open(f"fitness{self.solutionID}.txt", "w") as f:
            f.write(str(self.fitness))






