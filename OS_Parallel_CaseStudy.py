"""
  _____                 _ _            _      _____                          _   _             
 |  __ \               | | |          | |    |  __ \                        | | (_)            
 | |  | | ___  __ _  __| | | ___   ___| | __ | |__) | __ _____   _____ _ __ | |_ _  ___  _ __  
 | |  | |/ _ \/ _` |/ _` | |/ _ \ / __| |/ / |  ___/ '__/ _ \ \ / / _ \ '_ \| __| |/ _ \| '_ \ 
 | |__| |  __/ (_| | (_| | | (_) | (__|   <  | |   | | |  __/\ V /  __/ | | | |_| | (_) | | | |
 |_____/ \___|\__,_|\__,_|_|\___/ \___|_|\_\ |_|   |_|  \___| \_/ \___|_| |_|\__|_|\___/|_| |_|
"""
'''
Author: Villanueva Francis 


'''

'''

This is a simple implementation of deadlocks with the use of Python.
Deadlocks is a situation in an operating system where a group of processes
are being held by other processes in the group.
'''

import matplotlib.pyplot as plt

#important variables
processes = []
memory_blocks = []

lenProcesses = int(0)
lenMemory = int(0)

def validate_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
        except ValueError:
            print("Invalid input. Please enter a valid number (greater than 0 and not a string).")

def insert_toArray(array, array_name):
    for i in range(len(array)):
        value = input("Enter the value for {} #{}: ".format(array_name, i+1))
        array[i] = value
    return array

#First fit
'''
searching through memory blocks from the beginning,
looking for the first block that can fit the process.
'''
def first_fit(memory_blocks, processes):
    allocation = [-1] * len(processes)
    
    for i, process in enumerate(processes):
        for j, block in enumerate(memory_blocks):
            if block >= process:
                allocation[i] = j
                memory_blocks[j] -= process
                break
    return allocation

#Best fit
'''
searches through the list of free blocks of memory
to find the block that is closest in size to
the memory request from the process.
'''
def best_fit(memory_blocks, processes):
    allocation = [-1] * len(processes)
    for i, process in enumerate(processes):
        best_index = -1
        for j, block in enumerate(memory_blocks):
            if block >= process:
                if best_index == -1 or memory_blocks[j] < memory_blocks[best_index]:
                    best_index = j
        if best_index != -1:
            allocation[i] = best_index
            memory_blocks[best_index] -= process
    return allocation

#Worst fit
'''
process traverses the whole memory and always
search for the largest partition, and then
the process is placed in that hole/partition.
'''
def worst_fit(memory_blocks, processes):
    allocation = [-1] * len(processes)
    for i, process in enumerate(processes):
        worst_index = -1
        for j, block in enumerate(memory_blocks):
            if block >= process:
                if worst_index == -1 or memory_blocks[j] > memory_blocks[worst_index]:
                    worst_index = j
        if worst_index != -1:
            allocation[i] = worst_index
            memory_blocks[worst_index] -= process
    return allocation


#Banker's Algorithm
def bankers_algorithm(available, max_demand, allocation):
    processes = len(allocation)
    resources = len(available)

    need = [[max_demand[i][j] - allocation[i][j] for j in range(resources)] for i in range(processes)]
    finish = [False] * processes
    safe_sequence = []

    work = available[:]

    while len(safe_sequence) < processes:
        found = False
        for i in range(processes):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(resources)):
                for j in range(resources):
                    work[j] += allocation[i][j]
                finish[i] = True
                safe_sequence.append(i)
                found = True
                break
        if not found:
            return False, []
    return True, safe_sequence

print("Memory Allocation Algorithms (first fit, best fit, worst fit):\n")

#User gets to input the number of processes and memory blocks
lenProcesses = int(input("Enter the number of processes: "))
processes = insert_toArray([None] * lenProcesses, 'process')
processes = list(map(int, processes))

print("\nPrcesses: ", processes, "\n")

lenMemory = validate_input("Enter the number of memory blocks: ")
memory_blocks = insert_toArray([None] * lenMemory, "memory block")
memory_blocks = list(map(int, memory_blocks))

print("\nMemory Blocks: ", memory_blocks, "\n")

#First fit, Best fit, Worst fit
ff = first_fit(memory_blocks.copy(), processes)
bf = best_fit(memory_blocks.copy(), processes)
wf = worst_fit(memory_blocks.copy(), processes)

print("First Fit Allocation:", ff)
print("Best Fit Allocation:", bf)
print("Worst Fit Allocation:", wf)

#plotting results
labels = []

#flexible enough to handle any number of processes
for i in range(1, lenProcesses + 1):
    labels.append(f"P{i}")

fig, ax = plt.subplots()
bar_width = 0.2
x = range(len(processes))

ax.bar([p - bar_width for p in x], ff, width=bar_width, label='First Fit', color='#4E79A7')
ax.bar(x, bf, width=bar_width, label='Best Fit', color='#F28E2B')
ax.bar([p + bar_width for p in x], wf, width=bar_width, label='Worst Fit', color='#EDC948')

ax.set_xlabel('Processes')
ax.set_ylabel('Block Index Allocated')
ax.set_title('Memory Allocation Comparison')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
plt.savefig("process_allocation.png")
plt.show()

#Banker's Algorithm
'''
Banker's algorithm is used for resource allocation and deadlock avoidance
algorithm in opearing systems developed by Edsger Dijikstra.
It ensures that a system remains in a safe state by carefully
allocating resources to processes while avoiding unsafe states
that could lead to deadlocks.
'''

print("Bankers Algorithm:\n")

available = [5, 4, 1]
demand = [[8, 6, 2], [4, 3, 1], [7, 2, 3], [3, 2, 1], [6, 4, 2]]
alloc = [[1, 2, 0], [3, 1, 0], [2, 0, 1], [1, 1, 1], [0, 1, 1]]

safe, sequence = bankers_algorithm(available, demand, alloc)
if safe:
    print("System is in a safe state.")
    print("Safe sequence:", sequence)

    fig3, ax3 = plt.subplots(figsize=(8, 2))
    
    for i, p in enumerate(sequence):
        ax3.broken_barh([(i, 1)], (10, 9), facecolors='#663399')
        ax3.text(i + 0.5, 14, f'P{p}', ha='center', va='center', color='white', fontsize=10)
    
    ax3.set_ylim(5, 25)
    ax3.set_xlim(0, len(sequence))
    ax3.set_xlabel('Execution Order')
    ax3.set_yticks([])
    ax3.set_title('Banker\'s Algorithm Safe Sequence')
    ax3.grid(True, axis='x', linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig("sequence_chart.png")
    plt.show()

else:
    print("System is in an unsafe state and is unable to continue.")
    print("Deadlock detected.")
