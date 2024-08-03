# ECE652S24_FinalExam

ECE652S24Take-Home Final Exam

# What to do in this proj.

Your objective is to implement a simulator for the Deadline Monotonic scheduling algorithm on a single-core CPU. Your solution should be a Python3 program. Your program will read a set of periodic tasks from a file and report if the task set is schedulable under Deadline Monotonic, as well as the number of times each task is preempted per hyperperiod.

# My algorithm

```
My algorithm, take workload1.txt as example,
T0 = [1,3,3], T1 = [2,4,5] as the input task set.
Manage to data for the task set:
1. available time resource, T_available
2. task required time resource, T_required


First interation, allocate time resource to T0, because T0 has the highest priority
1. available time resource,  T_available= [0,12] meaning from 0.000 to 12.000 (in 0.0001 percision as the homework required)
2. task T0 required time resource, T_required =
    in [0, 3] asks for time length of 1.000
    in [3, 6] asks for time length of 1.000
    in [6, 9] asks for time length of 1.000
    in [9, 12] asks for time length of 1.000

allocate time resource from available time resource according to T_required,
3. allocated time resource T_allocated = [[0,1], [3,4], [6,7], [9,10]], which is:
    in [0, 3] allocate [0,1], successfully
    in [3, 6] allocate [3,4], successfully
    in [6, 9] allocate [6,7], successfully
    in [9, 12] allocate [9,10], successfully
4. update the new T_available = [[1,3], [4,6], [7,9], [10, 12]]


Second interation, allocate time time resource to second highest priority task, which is T1.
1. T_available = [[1,3], [4,6], [7,9], [10, 12]]  (which was updated in last interation)
2. T1's T_required =
    in [0,5] asks for time length of 2.000
    in [4,9] asks for time length of 2.000
    in [8,12] asks for time length of 2.000

allocate time resource from available time resource according to T1's T_required,
3. allocated time resource for T1, T_allocated = [[1,3], [4,6], [8,9], [10,11]], which is:
    in [0,5] allocate [1,3], successfully
    in [4,9] allocate [4,6], successfully
    in [8,12] allocate  [8,9], [10,11], successfully, here there are two time slots, so there is one preemption.
4. update the new T_available = [[7,8], [11,12]]

With in two iteration, my algorithm can allocate time resource basing on Deadline Monotonic.
start with data:

class Task:
    def __init__(self, execution_time, period, deadline):
        self.execution_time = execution_time
        self.period = period
        self.deadline = deadline
        self.preemptions = 0
        self.t_required = []
        self.t_allocated = []

T0 = Task(1.000, 3.000, 3.000)
T1 = Task(2.000, 4.000, 5.000)
tasks = [T0, T1]
T_available = [[0,12]]



T_available = [[1,3], [4,6], [7,9], [10, 12]]
T_required = [[0, 5], [4, 9], [8, 12]]
execution_time = 2.0
Expected result: T_allocated = {[0, 5]:[1,3], [4, 9]: [4,6], [8, 12]: [8,9], [10,11]}

```
