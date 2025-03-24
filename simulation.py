import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import constants as c
import time
import numpy
from world import WORLD
from robot import ROBOT

class SIMULATION:
    def __init__(self, directOrGUI):
        if directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, c.GRAVITY)

        self.world = WORLD()
        self.robot = ROBOT()
    
    def Run(self):
        for t in range(c.SIMULATION_STEPS):
            #print(f"Iteration number: {t}")
            p.stepSimulation()  # Keep the simulation running
            self.robot.Sense(t)  # Step 8: Call Sense() method after simulation step
            self.robot.Think()
            self.robot.Act(t)  # Step 9: Call Act() method to perform actions
            time.sleep(c.TIME_STEP)  # Maintain real-time speed
        
        # Step 10: Save sensor and motor values
        self.robot.Save_Values()

    def Get_Fitness(self):
        # Get info about the robots final state
        self.robot.Get_Fitness()
    
    # Step 4: Add destructor to disconnect from PyBullet
    def __del__(self):
        p.disconnect()
