import pybullet as p

class WORLD:
    def __init__(self):
        # Load the floor (plane)
        self.planeId = p.loadURDF("plane.urdf")

        # Load the world from SDF file
        p.loadSDF("world.sdf")
