import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV log
df = pd.read_csv("fitness_log.csv", header=None, names=["ID", "Distance", "Time", "Fitness"])

# Plot the performance (Distance vs Time)
plt.figure(figsize=(10, 6))
plt.scatter(df["Distance"], df["Time"], c="blue", label="Robot Performance")

# Highlight the best-performing robot (highest fitness)
best = df.sort_values("Fitness", ascending=False).iloc[0]
plt.scatter(best["Distance"], best["Time"], c="red", s=100, edgecolors='black', label="Best Robot")

# Styling and labels
plt.title("Robot Efficiency in Navigating Obstacle Grid", fontsize=14)
plt.xlabel("Distance Traveled Through Grid (x)", fontsize=12)
plt.ylabel("Time to Exit (seconds)", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()

# Save the plot 
# plt.savefig("robot_performance_plot.png", dpi=300)

# Show the plot
plt.show()
