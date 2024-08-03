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
class Task:
    def __init__(self, execution_time, period, deadline):
        self.execution_time = execution_time
        self.period = period
        self.deadline = deadline
        self.preemptions = 0
        self.t_required = self.calculate_required_times()
        self.t_allocated = []

    def calculate_required_times(self):
        t_required = []
        time = 0
        while time + self.period <= 12:
            t_required.append((time, time + self.deadline))
            time += self.period
        return t_required

    def __repr__(self):
        return (f"Task(execution_time={self.execution_time}, period={self.period}, "
                f"deadline={self.deadline}, preemptions={self.preemptions}, "
                f"t_required={self.t_required}, t_allocated={self.t_allocated})")
    

"""
it handles one required time slot at a time. The function will find the necessary 
available time slots to fulfill the required execution time within the specified 
required interval.
"""
def allocate_time_to_task(T_available, T_required, execution_time):
    T_allocated = {tuple(interval): [] for interval in T_required}
    remaining_execution_time = execution_time

    for (start, end) in T_required:
        if remaining_execution_time <= 0:
            break
        new_T_available = []
        for (a_start, a_end) in T_available:
            if a_end <= start or a_start >= end:
                new_T_available.append([a_start, a_end])
            else:
                if a_start < start:
                    new_T_available.append([a_start, start])
                alloc_start = max(a_start, start)
                alloc_end = min(a_end, end)
                while remaining_execution_time > 0 and alloc_start < alloc_end:
                    allocation_length = min(remaining_execution_time, alloc_end - alloc_start)
                    T_allocated[(start, end)].append([alloc_start, alloc_start + allocation_length])
                    remaining_execution_time -= allocation_length
                    alloc_start += allocation_length
                    if alloc_start < a_end:
                        new_T_available.append([alloc_start, a_end])
                if remaining_execution_time <= 0:
                    break
        T_available = new_T_available
    
    return T_allocated

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


def test_allocate_time():
    # Initialize tasks
    T0 = Task(1.000, 3.000, 3.000)
    T1 = Task(2.000, 4.000, 5.000)
    tasks = [T0, T1]

    # Test example1
    T_available = [[1, 3], [4, 6], [7, 9], [10, 12]]
    T_required = [0, 5]
    execution_time = 2.0

    IsOK, T_allocated = allocate_time_to_task(T_available, T_required, execution_time)
    print("T_allocated:", T_allocated) # expect T_allocated=[1,3]

    # Test example2
    T_available = [[1, 3], [4, 6], [7, 9], [10, 12]]
    T_required = [4, 9]
    execution_time = 2.0

    T_allocated = allocate_time_to_task(T_available, T_required, execution_time)
    print("T_allocated:", T_allocated) # expect T_allocated=[4,6], IsOK=true
        
    # Test example3
    T_available = [[1, 3], [4, 6], [7, 9], [10, 12]]
    T_required = [8, 12]
    execution_time = 2.0

    T_allocated = allocate_time_to_task(T_available, T_required, execution_time)
    print("T_allocated:", T_allocated) # expect T_allocated=[[8,9],[10,12]]


def main():
    # if len(sys.argv) != 2:
    #     print("Usage: python3 ece_652_final.py <input_file>")
    #     return

    # filename = sys.argv[1]
    # read_file_to_list(filename) # read file and extract data to 'tasks'
    # print(tasks)
    test_allocate_time()


## run the main here.
if __name__ == '__main__':
    main()

