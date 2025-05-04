from solution import SOLUTION
import constants as c
import copy
import os

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        self.parents = {}
        self.children = {}
        self.nextAvailableID = 0

        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve_For_One_Generation(self):
        # Step 0: Evaluate initial parents if they haven't been evaluated yet
        if any(parent.fitness is None for parent in self.parents.values()):
            self.Evaluate(self.parents)

        # Step 1: Create and mutate children
        self.Spawn()
        self.Mutate()

        # Step 2: Evaluate children
        self.Evaluate(self.children)

        # Step 3: Select better solutions
        self.Select()

        # Step 4: Log best fitness of current generation
        self.Log_Best_Fitness()

        # Step 5: Optional debug print
        self.Print()

    def Spawn(self):
        self.children = {}
        for key in self.parents:
            self.children[key] = copy.deepcopy(self.parents[key])
            self.children[key].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for child in self.children.values():
            child.Mutate()

    def Evaluate(self, solutions):
        for s in solutions.values():
            s.Start_Simulation("DIRECT")
        for s in solutions.values():
            s.Wait_For_Simulation_To_End()

    def Select(self):
        best_key = max(self.parents, key=lambda k: self.parents[k].fitness)
        best_parent = self.parents[best_key]  # save best

        for key in self.parents:
            if self.children[key].fitness > self.parents[key].fitness:
                self.parents[key] = self.children[key]

        # Restore best parent
        self.parents[best_key] = best_parent

    def Print(self):
        for key in self.parents:
            print(f"Parent {key} fitness: {self.parents[key].fitness} | Child {key} fitness: {self.children[key].fitness}")

    def Log_Best_Fitness(self):
        best_fitness = max(parent.fitness for parent in self.parents.values())

        # Determine file name based on fitness type
        suffix = "A" if c.FITNESS_TYPE == "A" else "B"
        filename = f"fitness_log_{suffix}.csv"

        with open(filename, "a") as f:
            f.write(f"{best_fitness}\n")

    def Show_Best(self):
        best = max(self.parents.values(), key=lambda p: p.fitness)
        print(f"The best fitness found was: {best.fitness}")
        print(f"The best robot ID was: {best.myID}")
        
        # Save robot ID, body file, and world file for simulate.py
        with open("best_robot_info.txt", "w") as f:
            f.write(f"{best.myID},body{best.myID}.urdf,world{best.myID}.sdf\n")
        
        best.Start_Simulation("GUI")