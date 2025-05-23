import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from sys import argv

try:
    test_directory: str = argv[1]
except IndexError:
    test_directory: str = '' 

# Read times from file
data = {
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

for key, values in data.items():
    plt.plot(range(len(values)), values, label=key)
plt.xlabel('Test Case')
plt.ylabel('Time (seconds)')
plt.title('Speed Comparison of Programming Languages')
plt.legend()
plt.grid()
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
# Save plot automatically (optional)
plt.savefig(f'{test_directory}benchmark_results.png', dpi=600, bbox_inches='tight')  # Saves as PNG
plt.show()
