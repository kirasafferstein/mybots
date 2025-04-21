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
        self.robot.start_time = time.time()  # just for logging/debugging

        for t in range(c.SIMULATION_STEPS):
            p.stepSimulation()
            self.robot.Sense(t)
            self.robot.Track_Collisions()

            self.robot.Think()
            self.robot.Act(t)

            # ✅ Check if goal is reached and break early
            x = p.getBasePositionAndOrientation(self.robot.robotId)[0][0]
            if x >= c.GOAL_X:
                print(f"[DEBUG] Robot {self.robot.solutionID} reached goal at x={x:.2f} on step {t}")
                self.robot.current_time_step = t  # record step for fitness
                break

            if self.directOrGUI == "GUI":
                time.sleep(c.TIME_STEP)

        # 🧱 If robot didn’t exit early, set to max time
        if not hasattr(self.robot, "current_time_step"):
            self.robot.current_time_step = c.SIMULATION_STEPS

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
