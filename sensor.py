import numpy
import pyrosim.pyrosim as pyrosim
import constants as c

class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName  # Store the link name
        self.values = numpy.zeros(c.SIMULATION_STEPS)  # Step 9: Store sensor values vector
        #print(self.values)  # Step 10: Print vector before the simulation starts
    
    def Get_Value(self, t):
        self.values[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)  # Step 11: Store sensor value
        #if t == c.SIMULATION_STEPS - 1:
            #print(self.values)  # Step 12: Print values at last time step