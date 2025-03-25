from solution import SOLUTION
import constants as c
import copy
import os
import time

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        #self.parent = SOLUTION()  # Create an instance of SOLUTION

        self.parents = {}
        self.nextAvailableID = 0


        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

        print("All parent IDs:", list(self.parents.keys()))


    def Evolve(self):
        #self.parent.Evaluate("GUI")

        #for currentGeneration in range(c.numberOfGenerations):
         #   self.Evolve_For_One_Generation()

        # Step 1: Launch all parents in background
        for key in self.parents:
            print(f"Evaluating parent {key}...")
            self.parents[key].Start_Simulation("DIRECT")
            
        for key in self.parents:
            self.parents[key].Wait_For_Simulation_To_End()

        self.Evolve_For_One_Generation()

        '''
        # Step 2: Wait for all fitness files to show up
        for key in self.parents:
            fitnessFileName = f"fitness{self.parents[key].myID}.txt"
            print(f"Waiting for {fitnessFileName}...")
            while not os.path.exists(fitnessFileName):
                time.sleep(0.01)

            with open(fitnessFileName, "r") as fitnessFile:
                self.parents[key].fitness = float(fitnessFile.read())

            os.system(f"del {fitnessFileName}")
            print(f"fitness{key}.txt found and read!")'
        '''


    def Evolve_For_One_Generation(self):
        #self.Spawn()
        #self.Mutate()
        #self.child.Evaluate("GUI")
        #self.Print()
        #self.Select()
        pass

    def Spawn(self):
        self.children = {}

        for key in self.parents:
            self.children[key] = copy.deepcopy(self.parents[key])
            self.children[key].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        self.child.Mutate()

    def Select(self):
         if self.child.fitness < self.parent.fitness:
                self.parent = self.child

    def Print(self):
        print("Parent fitness:", self.parent.fitness, "| Child fitness:", self.child.fitness)

    def Show_Best(self):
       # self.parent.Create_World()
        #self.parent.Create_Body()
        #self.parent.Create_Brain()
        #self.parent.Evaluate("GUI")
        
        pass

