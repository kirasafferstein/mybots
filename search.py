import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
from generate import Create_World
import constants as c

# Wipe old fitness log
if os.path.exists("fitness_log.csv"):
    os.remove("fitness_log.csv")

Create_World()

phc = PARALLEL_HILL_CLIMBER()

for gen in range(c.numberOfGenerations):
    print(f"--- Generation {gen} ---")
    phc.Evolve_For_One_Generation()

phc.Show_Best()
