#!/bin/bash

# Output file
directory="while_loop_tests"
output_file="$directory/times.txt"

py_file="$directory/times/python.txt"
c_file="$directory/times/c.txt"
java_file="$directory/times/java.txt"
csharp_file="$directory/times/c#.txt"
cpp_file="$directory/times/c++.txt"

# > "$output_file"  # Clear file

# Define programs
declare -A programs=(
    ["Python"]="python3 $directory/scripts/while_loop.py" # sum_python.py
    ["Java"]="java $directory/scripts/while_loop.java"
    ["CSharp"]="dotnet run --project $directory/scripts/while_loop.sc"
    ["C"]="gcc $directory/scripts/while_loop.c"
    ["C++"]="cpp $directory/scripts/while_loop.cpp"
)

# Colors
GREEN="\e[32m"
RED="\e[31m"
YELLOW="\e[33m"
BLUE="\e[34m"
RESET="\e[0m"

# Spinner function
spin() {
    local pid=$!
    local delay=0.1
    local spinstr='|/-\'
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Run each program
for lang in "${!programs[@]}"; do
    echo -ne "${BLUE}Running $lang...${RESET}"

    # Get the command part only (first word)
    cmd=$(echo "${programs[$lang]}" | awk '{print $1}')

    # Check if the command exists
    if ! command_exists "$cmd"; then
        echo -e "${RED} Failed! ($cmd not found)${RESET}"
        continue
    fi

    # Run and measure time
    { time ${programs[$lang]} > /dev/null; } 2> temp_time.txt &
    spin
if [ $? -eq 0 ]; then
    real_time=$(grep real temp_time.txt | awk '{print $2}')

    if [ -z "$real_time" ]; then
        echo -e "${RED} Failed to measure time. Skipping.$RESET"
        continue
    fi

    min=$(echo "$real_time" | cut -dm -f1)
    sec=$(echo "$real_time" | cut -dm -f2 | tr -d s)

    total_seconds=$(echo "$min*60 + $sec" | bc 2>/dev/null)

    if [ -n "$total_seconds" ]; then
        echo -e "${GREEN} Done! (${total_seconds}s)${RESET}"
        echo "$lang $total_seconds" >> "$output_file"
    else
        echo -e "${RED} Failed to compute total time. Skipping.$RESET"
    fi
else
    echo -e "${RED} Failed during execution!${RESET}"
fi
done

# Cleanup
rm -f temp_time.txt

# Check if plot_results.py exists
if [ -f plot_results.py ]; then
    echo -e "\n${YELLOW}Generating plot...${RESET}"
    python3 plot_results.py while_loop_tests/
    echo -e "${GREEN}Plot saved as benchmark_results.png.${RESET}"
    echo -e "\n${YELLOW}Generating averages plot...${RESET}"
    python3 plot_average.py while_loop_tests/
    echo -e "${GREEN}Plot saved as averages.png.${RESET}"
    # echo -e "${YELLOW}running web server${RESET}"
    # python3 flask_server.py --folder while_loop_tests/
else
    echo -e "\n${RED}plot_results.py not found. Skipping plot generation.${RESET}"
fi

echo -e "\n${YELLOW}All tasks completed.${RESET}"
