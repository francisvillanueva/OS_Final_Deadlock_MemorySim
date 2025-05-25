# OS_Final_Deadlock_MemorySim
OS and Parallel Programming Final Project

<h1><strong>Title: <ins>Simulating and Analyzing Deadlock and Memory Allocation Strategies in Operating Systems</ins></strong></h1>
<p>  </p>

##technology used:
- Python
- Matplotlib for visualization
  
<h2> Description: </h2>
<p> &nbsp;&nbsp;&nbsp;&nbsp; This project explores key operating system concepts by simulating memory allocation strategies—<strong>First Fit, Best Fit, and Worst Fit</strong>—alongside the <strong>Banker’s Algorithm</strong> for deadlock avoidance. Implemented in Python, the simulation models how processes request and release memory or resources. The project includes visualizations using the `matplotlib.pyplot` to illustrate allocation efficiency and system safety under different conditions, providing insights into performance trade-offs and resource management. </p>

<h2> Team Members: </h2>
  
<h3><a href="https://github.com/carendeperalta"> De Peralta, Caren Elizabeth </a></h3>
<p> Report Writing, Theory Review </p>
<h3><a href="https://github.com/Terrrrrrrrrrrrrrrrr"> Russel, Lester Jhon </a></h3>
<p> Video Editing and Final Polishing </p>
<h3><a href="https://github.com/vdenilin"> Vidallo, Denilin </a></h3>
<p> Documentation and Testing Support </p>
<h3><a href="https://github.com/francisvillanueva"> Villanueva, Francis Niño </a></h3>
<p> Programming & Algorithm Implementation </p>
  
<h2> Screenshots and Code Explanation: </h2>
<div align="center">
  <h2><strong> Memory Allocation </strong></h2>
</div>

<h3> First Fit Algorithm </h3>

``` python
def first_fit(memory_blocks, processes):
    allocation = [-1] * len(processes)
    
    for i, process in enumerate(processes):
        for j, block in enumerate(memory_blocks):
            if block >= process:
                allocation[i] = j
                memory_blocks[j] -= process
                break
    return allocation
```

<p> First fit searches through memory blocks from the beginning, looking for the first block that can fit the process. </p>
<p> &nbsp;&nbsp;&nbsp;&nbsp; This function <code>first_fit</code> accepts the <code>memory_blocks</code> and <code>processes</code> variable and makes an array <code>allocation</code> that has the size length of the array <code>processes</code> and loops through <code>memory_block</code> looking for the <strong>first</strong> <code>block</code> that can accommodate the <code>process</code> that is the first available <code>block</code> large enough to fit the <code>process</code>. </p>


<h3> Best Fit </h3>

``` python
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
```

<p> Best fit searches through the list of free blocks of memory to find the block that is closest in size to the memory request from the process. </p>
<p> &nbsp;&nbsp;&nbsp;&nbsp; Same with the <code>first_fit</code>, <code>best_fit</code> accepts the <code>memory_blocks</code> and <code>processes</code> variable and makes an array <code>allocation</code> that has the size length of the array <code>processes</code> and loops through <code>memory_block</code> looking for the <strong>smallest available <code>block</code> but large enough</strong> that can accommodate the <code>process</code> through all <code>memory_blocks</code> leaving the smallest remaining free space. </p>

<h3> Worst Fit Algorithm </h3>

``` python
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
```

<p> Worst fit process traverses the whole memory and always searches for the largest partition, and then the process is placed in that hole/partition. </p>
<p> &nbsp;&nbsp;&nbsp;&nbsp; like the other functions <code>first_fit</code> and <code>best_fit</code>, the function <code>worst_fit</code> function accepts the <code>memory_blocks</code> and <code>processes</code> variable and makes an array <code>allocation</code> that has the size length of the array <code>processes</code> and loops through <code>memory_block</code> finding and <strong>allocates the largest available <code>block</code> that is large enough</strong> to fit the <code>process</code>, searching through the <code>memory_blocks</code> to find the one that leaves the largest remaining free space. </p>


<pre>
  <h3> OUTPUT from Pyplot </h3>
  <div align="center">
    <img src="https://github.com/francisvillanueva/OS_Final_Deadlock_MemorySim/blob/main/process_allocation.png">
  </div>
</pre>

<div align="center">
  <h2><strong> Banker's Algorithm </strong></h2>
</div>

``` python
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
```

<p> Banker's Algorithm ensures that a system remains in a safe state by carefully allocating resources to processes while avoiding unsafe states that could lead to deadlocks. </p>
<p> &nbsp;&nbsp;&nbsp;&nbsp; The <code>bankers_algorithm</code> accepts the variables <code>available</code>, <code>max_demand</code> and <code>allocation</code> and gets the length of the 3d arrays code>available</code> and <code>allocation</code>, calculates how much more each <code>process</code> may need using the <code>need</code> 3D array using the difference between <code>max_demand</code> and <code>allocation</code>. the function attempts to find a safe sequence of <code>processes</code> without leading to a deadlock, looping through and checking each unfinished <code>processes</code> can complete with the currently available <code>resources</code>. if all processes are safely completed, the function returns <code>True</code> with the array <code>safe_sequence</code> or else it will return <code>False</code></p>
<pre>
  <h2> OUTPUT from Pyplot </h2>
  <div align="center">
    <img src="https://github.com/francisvillanueva/OS_Final_Deadlock_MemorySim/blob/main/sequence_chart.png">
  </div>  
</pre>


