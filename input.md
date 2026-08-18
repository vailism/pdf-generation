---
title: Operating Systems Study Guide
subtitle: CPU Scheduling Algorithms & Deadlocks
theme: random
author: Vailism
filename: OS_Unit3_Study_Guide.pdf
---

# 1. Overview & Core Concepts
CPU Scheduling is the process by which the operating system decides which of the ready processes is allocated the CPU for execution.

> [!DEFINITION] CPU Scheduling: The mechanism of allocating CPU time among ready-to-run processes to maximize system throughput and resource utilization.

> [!ANALOGY] Think of CPU Scheduling like an airport runway with multiple flights waiting to take off. The Air Traffic Controller (the OS Scheduler) determines which airplane (process) gets clearance on the runway (CPU).

# 2. Scheduling Criteria & Performance Metrics
To evaluate and compare different scheduling algorithms, standard performance metrics are used:

| Metric | Formula | Goal |
|---|---|---|
| Turnaround Time (TAT) | TAT = Completion Time - Arrival Time | Minimize |
| Waiting Time (WT) | WT = Turnaround Time - Burst Time | Minimize |
| Response Time (RT) | RT = First CPU Start Time - Arrival Time | Minimize |
| CPU Utilization | (Busy Time / Total Time) * 100 | Maximize |
| Throughput | Processes Completed / Total Time | Maximize |

> [!FORMULA] TAT = CT - AT  |  WT = TAT - BT  |  RT = First Start Time - AT

# 3. Necessary Conditions for Deadlock
A deadlock occurs when a set of processes are blocked because each process is holding a resource and waiting for another resource held by some other process.

- Mutual Exclusion: Resources cannot be shared simultaneously.
- Hold and Wait: A process holds at least one resource and is waiting for others.
- No Preemption: Resources cannot be forcibly seized from a process.
- Circular Wait: A closed loop of processes where each holds a resource needed by the next.

> [!MEMORY_TRICK] Remember **M-H-N-C**: **M**utual exclusion, **H**old & wait, **N**o preemption, **C**ircular wait. All 4 MUST hold simultaneously for deadlock!

# 4. Exam Template Questions & Answers

Q: Differentiate Deadlock Prevention, Avoidance, and Detection.
A: Prevention permanently eliminates at least one of the four necessary conditions. Avoidance dynamically checks resource requests to ensure system stays in a safe state (e.g. Banker's Algorithm). Detection permits deadlocks to occur, periodically audits resource graphs, and initiates recovery when found.
