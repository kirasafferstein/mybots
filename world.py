import pybullet as p

class WORLD:
    def __init__(self):
        # Load the floor (plane)
        self.planeId = p.loadURDF("plane.urdf")

        # Try loading the SDF world model
        try:
            p.loadSDF("world.sdf")
            print("World loaded successfully.")
        except Exception as e:
            print(f"Error loading world: {e}")