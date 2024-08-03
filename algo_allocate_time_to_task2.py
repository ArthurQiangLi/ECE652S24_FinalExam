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

# Test example1
T_available = [[1, 3], [4, 6], [7, 9], [10, 12]]
T_required = [0, 5]
execution_time = 2.0

T_available, T_allocated, IsOK = allocate_time_to_task(T_available, T_required, execution_time)
print("#### T_allocated:", T_allocated, ">>>>>> IsOK:", IsOK) # expect T_allocated=[1,3]

# Test example2
#T_available = [[1, 3], [4, 6], [7, 9], [10, 12]]
T_required = [4, 9]
execution_time = 2.0

T_available, T_allocated, IsOK = allocate_time_to_task(T_available, T_required, execution_time)
print("#### T_allocated:", T_allocated, ">>>>>> IsOK:", IsOK) # expect T_allocated=[4,6]
    
# Test example3
T_available = [[1, 3], [4, 6], [7, 9], [10, 12]]
T_required = [8, 12]
execution_time = 2.0

T_available, T_allocated, IsOK = allocate_time_to_task(T_available, T_required, execution_time)
print("#### T_allocated:", T_allocated, ">>>>>> IsOK:", IsOK) # expect T_allocated=[[8,9],[10,12]]
