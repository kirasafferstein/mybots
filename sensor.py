import numpy
import pyrosim.pyrosim as pyrosim
import constants as c

class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName
        self.values = numpy.zeros(c.SIMULATION_STEPS)
        self.value = 0  # <-- latest value

    def Get_Value(self, t):
        self.value = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        self.values[t] = self.value