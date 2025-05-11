import matplotlib.pyplot as plt
from sys import argv

try:
    test_directory: str = argv[1]
except IndexError:
    test_directory: str = '' 

# Read times from file
data:dict[str, list[float]] = {
    'Python': [],
    'Java': [],
    'C++': [],
    'CSharp': [],
    'C': []
}

with open(f'{test_directory}/times.txt', 'r') as f:
    for line in f:
        try:
            lang, time = line.strip().split()
            data[lang].append(float(time))
        except ValueError:
            pass

averages = [round(sum(i)/len(i), 3) for i in data.values() ]
# Plot
plt.figure(figsize=(10, 6))
bars: plt.bar = plt.bar(data.keys(), averages, color='lightgreen')
plt.xlabel('Programming Language')
plt.ylabel('Time (seconds)')
plt.title('Speed Comparison of Programming Languages')
plt.grid(axis='y')

# Add labels
for bar, time in zip(bars, averages):
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, f'{time}', ha='center', va='bottom')



# Save plot automatically (optional)
plt.savefig(f'{test_directory}averages.png', dpi=600, bbox_inches='tight')  # Saves as PNG
plt.show()
