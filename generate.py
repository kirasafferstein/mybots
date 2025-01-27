import pyrosim.pyrosim as pyrosim

# Tell pyrosim name of the file where information should be stored
pyrosim.Start_SDF("box.sdf")


# Stores a box with initial position and length height and width 
pyrosim.Send_Cube(name="Box", pos=[0,0,0.5] , size=[1,1,1])

pyrosim.End()



