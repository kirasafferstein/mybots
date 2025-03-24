import numpy
import pybullet as p
import pyrosim.pyrosim as pyrosim
import constants as c

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName.decode("utf-8") if isinstance(jointName, bytes) else jointName
        self.jointIndex = int(pyrosim.jointNamesToIndices[self.jointName.encode("utf-8")])
        self.Prepare_To_Act()
    
    def Prepare_To_Act(self):
        self.motorValues = numpy.zeros(c.SIMULATION_STEPS)

        if "FrontLeg" in self.jointName:
            self.amplitude = c.frontLegAmplitude
            self.frequency = c.frontLegFrequency / 2
            self.offset = c.frontLegPhaseOffset
        else:
            self.amplitude = c.backLegAmplitude
            self.frequency = c.backLegFrequency
            self.offset = c.backLegPhaseOffset

        for t in range(c.SIMULATION_STEPS):
            time_scaled = t / (c.SIMULATION_STEPS / self.frequency)
            self.motorValues[t] = self.amplitude * numpy.sin(2 * numpy.pi * time_scaled + self.offset)
    
    def Set_Value(self, desiredAngle, robotId):
        #targetLocation = self.motorValues[desiredAngle]
        #print(f"Setting motor value for {self.jointName} (index {self.jointIndex}) to {desiredAngle}")

        
        p.setJointMotorControl2(
            bodyIndex=robotId,
            jointIndex=self.jointIndex,
            controlMode=p.POSITION_CONTROL,
            targetPosition=desiredAngle,
            force=c.MOTOR_MAX_FORCE
        )