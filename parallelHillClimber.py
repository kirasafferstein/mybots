from solution import SOLUTION
import constants as c
import copy
import os
import time

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        #self.parent = SOLUTION()  # Create an instance of SOLUTION

        os.system("del brain*.nndf")      
        os.system("del fitness*.txt")    

        self.parents = {}
        self.children = {}
        self.nextAvailableID = 0

        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1


    def Evolve(self):
        # Step 1: Launch all parents in background
        for key in self.parents:
            print(f"Evaluating parent {key}...")
            self.parents[key].Start_Simulation("DIRECT")
        
        for key in self.parents:
            self.parents[key].Wait_For_Simulation_To_End()

        # Step 2: Launch all children in background
        self.Spawn()  # Create children
        self.Mutate()  # Mutate children
        self.Evaluate(self.children)  # Evaluate children in parallel

        # Call to Evolve_For_One_Generation if needed, but commented out for now
        # self.Evolve_For_One_Generation()
        self.Print()

        self.Select()
        self.Print()

    def Evaluate(self, solutions):
        # Evaluate parents or children (depending on the argument passed)
        for key in solutions:
            print(f"Evaluating solution {key}...")
            solutions[key].Start_Simulation("DIRECT")
        
        for key in solutions:
            solutions[key].Wait_For_Simulation_To_End()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate()
        self.Print()
        #self.Select()
        pass

    def Spawn(self):
        # Create an empty dictionary to hold children
        self.children = {}

        # Iterate over all the parents
        for key in self.parents:
            # Deepcopy the parent to create a new child
            self.children[key] = copy.deepcopy(self.parents[key])
            
            # Assign a unique ID to the child and increment the nextAvailableID
            self.children[key].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        # Iterate through each child in self.children and mutate them
        for key, child in self.children.items():
            child.Mutate()
            print(f"Child {key} mutated.")

    def Select(self):
        for key in self.parents:
            # Compare fitness of parent and child
            parent_fitness = self.parents[key].fitness
            child_fitness = self.children[key].fitness

            # If child has better fitness, replace parent with child
            if child_fitness < parent_fitness:
                print(f"The Child {key} had better fitness than parent so the parent will be replaced.")
                self.parents[key] = self.children[key]  # Replace the parent with the child
            else:
                print(f"PThe parent {key} had better fitness than the child so it will stay. The fitness comparison was: Parent = {parent_fitness}, Child = {child_fitness}")

    def Print(self):
        # Print an empty line at the start
        print()
        print()

        # Iterate through parents and children and print their fitness values
        for key in self.parents:
            print(f"Parent {key} fitness: {self.parents[key].fitness} | Child {key} fitness: {self.children[key].fitness}")

        # Print an empty line at the end
        print()


    def Show_Best(self):
       # Step 1: Find the parent with the lowest fitness
        best_parent = None
        best_fitness = float('inf')  # Start with a very large fitness value

        for key in self.parents:
            if self.parents[key].fitness < best_fitness:
                best_fitness = self.parents[key].fitness
                best_parent = self.parents[key]

        # Step 2: Simulate the best parent with graphics
        print(f"The best fitness found was: {best_fitness}")
        best_parent.Start_Simulation("GUI")

