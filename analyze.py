import matplotlib.pyplot as plt

def read_fitness_log(filename):
    try:
        with open(filename, "r") as f:
            return [float(line.strip()) for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Warning: {filename} not found.")
        return []

# Read logs
fitness_A = read_fitness_log("fitness_log_A.csv")
fitness_B = read_fitness_log("fitness_log_B.csv")

# Plot
plt.figure(figsize=(10, 6))
plt.plot(fitness_A, label="Fitness Function A", marker='o')
plt.plot(fitness_B, label="Fitness Function B", marker='s')

plt.xlabel("Generation")
plt.ylabel("Best Fitness")
plt.title("A/B Test: Fitness Over Generations")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
