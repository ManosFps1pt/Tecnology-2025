from flask import Flask, render_template, redirect, url_for, request
import subprocess
import os
import csv
import logging
import sys

logging.basicConfig(
    filename='server.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Redirect print() and errors to the log file
sys.stdout = open('server.log', 'a')
sys.stderr = sys.stdout


app = Flask(__name__)

RESULTS_FILE = 'while_loop_tests/times.txt'
BENCHMARK_SCRIPT = os.path.abspath('./while_loop.sh')
RESET_SCRIPT = os.path.abspath('./reset.sh')
CSV_FILE = 'while_loop_tests/times.csv'

def load_results():
    results = []
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    results.append((parts[0], float(parts[1])))

    grouped = {}
    for lang, time in results:
        grouped.setdefault(lang, []).append(time)

    return grouped  # Dict[str, List[float]]

def generate_csv():
    data = load_results()
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data.keys())
        try: 
            for i in range(len(list(data.values())[0])):
                row = []
                for lang in data.keys():
                    if i < len(data[lang]):
                        row.append(data[lang][i])
                    else:
                        row.append('')
                writer.writerow(row)
        except IndexError:
            pass

@app.route('/')
def home():
    generate_csv()
    results = csv.reader(open(CSV_FILE, 'r'))
    data = list(results)
    headers = data[0]
    data = data[1:]
    return render_template('home.html', headers=headers, rows=data)
    # return render_template('table.html', headers=headers, rows=data)
from flask import send_file

@app.route('/download')
def download_csv():
    generate_csv()
    return send_file(CSV_FILE, as_attachment=True)

@app.route('/line')
def show_line_plot():
    return render_template('show_image.html', path="/download_line", text="Line Plot of Benchmark Results")

@app.route('/average')
def show_average_plot():
    return render_template('show_image.html', path="/download_average", text="Average Benchmark Results")

@app.route('/download_line')
def download_line_plot():
    return send_file("while_loop_tests/benchmark_results.png", as_attachment=True)

@app.route('/download_average')
def download_average_plot():
    return send_file("while_loop_tests/averages.png", as_attachment=True)

@app.route('/run', methods=['POST'])
def run_benchmark():
    subprocess.run(BENCHMARK_SCRIPT, shell=True)
    return redirect(url_for('home'))

@app.route('/reset', methods=['POST'])
def reset():
    subprocess.run(RESET_SCRIPT, shell=True)
    return redirect(url_for('home'))

@app.route('/delete', methods=['POST'])
def delete_results():
    if os.path.exists(RESULTS_FILE):
        os.remove(RESULTS_FILE)
    if os.path.exists(CSV_FILE):
        os.remove(CSV_FILE)
    if os.path.exists("while_loop_tests/benchmark_results.png"):
        os.remove("while_loop_tests/benchmark_results.png")
    if os.path.exists("while_loop_tests/averages.png"):
        os.remove("while_loop_tests/averages.png")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
