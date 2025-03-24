import numpy
import matplotlib.pyplot 

# Load data/backLegSensorValues.npy into the vector backLegSensorValues
backLegSensorValues = numpy.load("data/backLegSensorValues.npy")
frontLegSensorValues = numpy.load("data/frontLegSensorValues.npy")
motorAngles = numpy.sin(numpy.linspace(0, 2 * numpy.pi, 1000)) * (numpy.pi /4)
frontLegMotorCommands = numpy.load("data/frontLegMotorCommands.npy")
backLegMotorCommands = numpy.load("data/backLegMotorCommands.npy")

# Draw the values in the vector 

# Front and back leg sensor values:
#matplotlib.pyplot.plot(backLegSensorValues, label = "Back Leg Sensors", linewidth = 2)
#matplotlib.pyplot.plot(frontLegSensorValues, label = "Front Leg Sensors", linewidth = 1)

# Motor angles:
#matplotlib.pyplot.plot(motorAngles, '--', label = "targetAngles", alpha = 0.5)

# Front and back motor commands
#matplotlib.pyplot.plot(backLegSensorValues, label="Back Leg Sensors", linewidth=2)
#matplotlib.pyplot.plot(frontLegSensorValues, label="Front Leg Sensors", linewidth=1)
matplotlib.pyplot.plot(backLegMotorCommands, '--', label="Back Leg Motor Commands", alpha=0.7)
matplotlib.pyplot.plot(frontLegMotorCommands, '--', label="Front Leg Motor Commands", linewidth=2)

# Make sure plot has legend
matplotlib.pyplot.legend()

# Show the plot
matplotlib.pyplot.show()



