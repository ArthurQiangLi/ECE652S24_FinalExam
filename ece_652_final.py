"""
Your objective is to implement a simulator for the Deadline Monotonic scheduling algorithm on a single-core CPU. 
Your solution should be a Python3 program. Your program will read a set of periodic tasks from a file and 
report if the task set is schedulable under Deadline Monotonic, as well as the number of times each task is 
preempted per hyperperiod.
* ece_652_final.py
* 1,3,2 precision up to 0.001, better use list to store each task
* In the event two tasks Ti and Tj have the same deadline, the lower identifier takes priority
***************************
Structure:
1-Read task from a file
2-Calculate hyperperiod
3-Sort task priority
4-Allocate time slots and count preemptions
5-Arrange the output
"""
from math import gcd
import sys

#******************************************************************************
## global data
tasks = []

#******************************************************************************

def lcm(a, b, precision=1e-5):
    if a == 0 or b == 0:
        return 0
    scale = 10 ** 5  # Scale to handle floating points
    a_scaled = int(a * scale)
    b_scaled = int(b * scale)
    result = abs(a_scaled * b_scaled) // gcd(a_scaled, b_scaled)
    return result / scale


def read_file_to_list(filename):
    global tasks #declare to use the global data
    tasks = []
    with open(filename, 'r') as file:
        for line in file:
            tasks.append(list(map(float, line.strip().split(',')))) ## parse as 'float' type data.
    return tasks


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 ece_652_final.py <input_file>")
        return

    filename = sys.argv[1]
    read_file_to_list(filename) # read file and extract data to 'tasks'
    print(tasks)



## run the main here.
if __name__ == '__main__':
    main()

