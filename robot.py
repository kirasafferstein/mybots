import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR
import constants as c
import numpy
from pyrosim.neuralNetwork import NEURAL_NETWORK # Include the NEURAL_NETWROK class from pyrosim

class ROBOT:
    def __init__(self):
        # Step 1: Load robot
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        
        # Step 2: Prepare sensors and motors
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

        # Create a nerual network (self.nn) and add any neurons and synapses to it from brain.nndf
        self.nn = NEURAL_NETWORK("brain.nndf")

    def Prepare_To_Sense(self):
        self.sensors = {}  # Initialize sensors dictionary
        
        # Step 3: Iterate over all links and create a sensor for each
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Prepare_To_Act(self):
        self.motors = {}  # Initialize motors dictionary

        print("Joints found in URDF:", [joint.decode("utf-8") for joint in pyrosim.jointNamesToIndices.keys()])  # Debugging line

        for jointName in pyrosim.jointNamesToIndices:
            decodedJointName = jointName.decode("utf-8")  # Convert byte string to regular string
            self.motors[decodedJointName] = MOTOR(decodedJointName)


    def Sense(self, t):
        for sensor in self.sensors.values():
            sensor.Get_Value(t)

    def Think(self):
        # Flow values from the sensors to the sensor neurons 
        self.nn.Update()
        self.nn.Print()
    
    def Act(self, t):
        #for neuronName in self.nn.Get_Neuron_Names():
            #if self.nn.Is_Motor_Neuron(neuronName):
                #jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                #desiredAngle = self.nn.Get_Value_Of(neuronName)

                # Set motor value using the motor neuron
                #jointName = jointName.encode("utf-8")  # Ensure it's stored as bytes
                #self.motors[jointName].Set_Value(desiredAngle, self)

                
                #print(neuronName, jointName, desiredAngle)

        #for motor in self.motors.values():
            #motor.Set_Value(t, self.robotId)

        print("Available motor joints:", self.motors.keys())  # Debugging line

        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)
                print(f"Motor Neuron {neuronName} is controlling joint {jointName} with desired angle {desiredAngle}.")
    
    def Save_Values(self):
        for linkName, sensor in self.sensors.items():
            numpy.save(f"data/{linkName}_sensorValues.npy", sensor.values)
        for jointName, motor in self.motors.items():
            numpy.save(f"data/{jointName}_motorValues.npy", motor.motorValues)