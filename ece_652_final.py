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
    T_allocated = []
    remaining_execution_time = execution_time
    r_start, r_end = T_required
    unused_T_available = []
    used_T_available = []                                   # to remove from T_available
    for (a_start, a_end) in T_available:
        if a_end <= r_start or a_start >= r_end:            # if there is NO overlap, sad
            continue                                        # skip this available slot
        else: # there is overlap between (r_start, r_end) and (a_start, a_end)
            used_T_available.append([a_start, a_end])       # to remove the available slot, (add back unused part later)
            if a_start < r_start:
                unused_T_available.append([a_start, r_start])  # this front part is not used, to return back to T_available
            olp_start = max(a_start, r_start)               # (olp_start, olp_end) is the overlapped part
            olp_end = min(a_end, r_end)                     #
            if remaining_execution_time > 0 and olp_start < olp_end: # eat time from overlapped part 
                allocation_length = min(remaining_execution_time, olp_end - olp_start) #in case ovealapped is very large
                T_allocated.append([olp_start, olp_start + allocation_length]) #eat only up to execution_time in overlapped part
                remaining_execution_time -= allocation_length
                olp_start += allocation_length
                if olp_start < a_end:
                    unused_T_available.append([olp_start, a_end]) # this rare part is not used, to return back to T_available
        if remaining_execution_time <= 0:
            break

    T_available = [item for item in T_available if item not in used_T_available]  #T_available - used_T_available
    T_available += unused_T_available                      # add back unused slots 
    T_available = sorted(T_available)                      #
    #print("T_available", T_available)

    IsOK = remaining_execution_time == 0
    return T_available, T_allocated, IsOK

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

