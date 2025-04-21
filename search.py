import os 
from parallelHillClimber import PARALLEL_HILL_CLIMBER 
from generate import Create_World

#for i in range(5):
#	os.system("py generate.py")
#	os.system("py simulate.py")

Create_World()

phc = PARALLEL_HILL_CLIMBER()
phc.Evolve()

phc.Show_Best()
