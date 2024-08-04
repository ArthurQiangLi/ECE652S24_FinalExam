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
import math
from functools import reduce
import sys

#******************************************************************************
## global data
tasks = []
g_hyperperiod = 0.0
ENABLE_DEBUG_PRINT = True   #Enable or disable debug print 

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
    global tasks # declare to use the global data
    tasks = []
    with open(filename, 'r') as file:
        for line_number, line in enumerate(file):
            execution_time, period, deadline = map(float, line.strip().split(','))
            task = Task(execution_time, period, deadline, line_number)
            tasks.append(task)
    return tasks


def debug_pring(msg):
    if(ENABLE_DEBUG_PRINT):
        print(msg)

class Task:
    def __init__(self, execution_time, period, deadline, index=0):
        self.index = index  #index in tasks, 0~len()-1
        self.execution_time = execution_time
        self.period = period
        self.deadline = deadline
        self.priority = 0 # to be calculated according to others
        self.t_required = []
        self.t_allocated = []
        self.is_feasible = False
        self.preemptions = 0


    def calculate_required_times(self, hyperperiod):
        t_required = []
        time = 0
        while time + self.period <= hyperperiod:
            t_required.append((time, time + self.deadline))
            time += self.period
        return t_required

    def __repr__(self):
        return (f"T{self.index}: e={self.execution_time}, per={self.period}, "
                f"d={self.deadline}, preem={self.preemptions}, prio={self.priority}"
                f"\n---- T_required={self.t_required}, \n---- T_allocated={self.t_allocated}"
                f"\n---- preemptions={self.preemptions}"
                "\n" + '.'*70 + f"feasible= {self.is_feasible}")
    

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

    IsOK = remaining_execution_time == 0
    return T_available, T_allocated, IsOK

def calculate_hyperperiod(tasks):
    periods = [task.period for task in tasks]
    return reduce(lambda x, y: x * y // math.gcd(int(x), int(y)), periods)

# def calculate_priorities(tasks):

def allocate_time_to_tasks(tasks):
# Just after get 'tasks' from reading a file
     #[1st, get hyperperiod, to let calculate T_required for each task]
    g_hyperperiod = calculate_hyperperiod(tasks)
    T_available = [[0, g_hyperperiod]] # todo calculate_hyperperiod()

    tasks.sort(key=lambda x: (x.deadline, x.index)) # calculate_priorities(tasks)    #1 Sort tasks by deadline (Deadline Monotonic)
    for i, t in enumerate(tasks):
        t.priority = i # assign priority from 0~len-1 to each task, for display use
        t.t_required = t.calculate_required_times(g_hyperperiod)

    is_feasible = True
    # [schedule for all tasks]
    for t in tasks:                 # Note tasks are in priority order
        for req in t.t_required:
            T_available, T_allocated, IsOK = allocate_time_to_task(T_available, req, t.execution_time)
            t.is_feasible = IsOK
            if not IsOK:
                is_feasible = False
                break; 
            t.preemptions += (len(T_allocated) - 1)
            t.t_allocated += T_allocated

    # [get preemptions list]
    preemptions = []
    if IsOK:
        tasks.sort(key=lambda x: x.index) # re-order to the task file line order
        for t in tasks:
            preemptions.append(t.preemptions)

    return is_feasible, preemptions


def print_task_allocations_report(tasks):
    print(f"hyperperiod = {g_hyperperiod}")

    for task in tasks:
        print("\n" + '-' * 80)
        print(f"{task}")


#******************************************************************************
def main():
    if len(sys.argv) != 2:
        print("Usage: python3 ece_652_final.py <input_file>")
        return

    filename = sys.argv[1]
    read_file_to_list(filename) # read file and extract data to 'tasks'
    is_ok, preemptions = allocate_time_to_tasks(tasks)
    # print_task_allocations_report(tasks)
    if is_ok:
        print("1")
        print(",".join(map(str, preemptions)))
    else:
        print("0")

## run the main here.
if __name__ == '__main__':
    main()

