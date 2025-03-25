import constants as c
import numpy

# Gravity
GRAVITY = -9.8

# Simulation Constants
SIMULATION_STEPS = 1000
#TIME_STEP = 1 / 60
TIME_STEP = 0.005

# Define motion parameters
backLegAmplitude = numpy.pi / 3 # Maximum joint angle
backLegFrequency = 10 # Number of cycles
backLegPhaseOffset = 0 # Phase shift

frontLegAmplitude = numpy.pi /4
frontLegFrequency = 12
frontLegPhaseOffset = numpy.pi / 2

# Motor Control
MOTOR_MAX_FORCE = 95

numberOfGenerations = 10

populationSize = 10
