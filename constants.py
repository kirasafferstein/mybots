import constants as c
import numpy

# Gravity
GRAVITY = -9.8

# Simulation Constants
SIMULATION_TIME = 45  # seconds
TIME_STEP = 1/240
SIMULATION_STEPS = int(SIMULATION_TIME / TIME_STEP)

GOAL_X = 25

# Define motion parameters
backLegAmplitude = numpy.pi / 3 # Maximum joint angle
backLegFrequency = 10 # Number of cycles
backLegPhaseOffset = 0 # Phase shift

frontLegAmplitude = numpy.pi /4
frontLegFrequency = 12
frontLegPhaseOffset = numpy.pi / 2

# Motor Control
MOTOR_MAX_FORCE = 150

#numberOfGenerations = 15
#populationSize = 15
numberOfGenerations = 8
populationSize = 8

FITNESS_TYPE = "B"

numSensorNeurons = 9  # Number of sensor neurons
numMotorNeurons = 8   # Number of motor neurons

