import matplotlib.pyplot as plt

# Open the log and grab the last value (fitness) from each line
with open("fitness_log.csv", "r") as f:
    fitness_values = [float(line.strip().split(",")[-1]) for line in f if line.strip()]

# Plot
plt.figure()
plt.plot(fitness_values, marker="o")
plt.xlabel("Generation")
plt.ylabel("Best Fitness")
plt.title("Fitness Improvement Over Generations")
plt.grid(True)
plt.tight_layout()
plt.show()
