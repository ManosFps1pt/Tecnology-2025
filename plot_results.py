import matplotlib.pyplot as plt
from sys import argv

try:
    test_directory: str = argv[1]
except IndexError:
    test_directory: str = '' 

# Read times from file
languages = []
times = []

with open(f'{test_directory}/times.txt', 'r') as f:
    for line in f:
        lang, time = line.strip().split()
        languages.append(lang)
        times.append(float(time))

# Plot
plt.figure(figsize=(10, 6))
bars = plt.bar(languages, times, color='lightgreen')
plt.xlabel('Programming Language')
plt.ylabel('Time (seconds)')
plt.title('Speed Comparison of Programming Languages')
plt.grid(axis='y')

# Add labels
for bar, time in zip(bars, times):
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, f'{time}', ha='center', va='bottom')

# Save plot automatically (optional)
plt.savefig(f'{test_directory}benchmark_results.png', dpi=300, bbox_inches='tight')  # Saves as PNG
plt.show()
