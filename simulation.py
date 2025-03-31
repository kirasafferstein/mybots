import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import constants as c
import time
import numpy
from world import WORLD
from robot import ROBOT

class SIMULATION:
    def __init__(self, directOrGUI, solutionID, bodyFile, worldFile):
        self.directOrGUI = directOrGUI
        self.physicsClient = p.connect(p.DIRECT if directOrGUI == "DIRECT" else p.GUI)
        
        if directOrGUI == "GUI":
            p.resetDebugVisualizerCamera(
            cameraDistance=20,      # Zoom out (increase to see more)
            cameraYaw=50,           # Rotate left/right
            cameraPitch=-30,        # Look down
            cameraTargetPosition=[4, 0, 0.5]  # Centered ahead of the robot
        )
        
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, c.GRAVITY)
        p.loadURDF("plane.urdf") # load floor

        # Load the custom world file
        p.loadSDF(worldFile)

        # Load the custom body file
        self.robot = ROBOT(solutionID, bodyFile)
    
    def Run(self):
        for t in range(c.SIMULATION_STEPS):
            p.stepSimulation()
            self.robot.Sense(t)
            self.robot.Think()
            self.robot.Act(t)

            # Only sleep if using GUI
            if self.directOrGUI == "GUI":
                time.sleep(c.TIME_STEP)

        self.robot.Save_Values()


    def Get_Fitness(self):
        # Get info about the robots final state
        self.robot.Get_Fitness()
    
    # Step 4: Add destructor to disconnect from PyBullet
    def __del__(self):
        p.disconnect()
        try:
            os.remove(bodyFile)
            os.remove(worldFile)
        except:
            pass  # In case files already deleted
