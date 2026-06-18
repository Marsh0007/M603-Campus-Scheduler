# M603 Campus Scheduler and Decision Support System

## Advanced Algorithms (M603) Project

### Overview

The Campus Scheduler and Decision Support System is designed to solve the university timetable scheduling problem using multiple algorithmic approaches.

The system automatically generates a conflict-free timetable while minimizing room-capacity waste and identifying scheduling issues that require manual intervention.

The project integrates four major algorithmic paradigms:

* Greedy Algorithms
* Graph Theory
* Dynamic Programming
* Recursive Backtracking

The scheduler considers:

* Professor conflicts
* Student group conflicts
* Room capacity constraints
* Capacity waste minimization
* Schedule quality evaluation
* Professor workload analysis

---

# Project Objectives

The objective of this project is to develop an intelligent scheduling system capable of:

1. Creating a valid university timetable.
2. Preventing professor scheduling conflicts.
3. Preventing student group scheduling conflicts.
4. Optimizing room assignments.
5. Reducing unused room capacity.
6. Providing conflict reports for manual review.
7. Supporting decision-making through schedule analytics.

---

# Project Structure

```text
M603_CampusScheduler/
│
├── data/
│   ├── constraints.json
│   └── constraints_stress.json
│
├── results/
│   └── final_schedule.json
│
├── src/
│   ├── main.py
│   ├── data_loader.py
│   ├── greedy_solver.py
│   ├── graph_engine.py
│   ├── optimizer.py
│   ├── backtracker.py
│   ├── validator.py
│   ├── conflict_analyzer.py
│   ├── quality_analyzer.py
│   ├── professor_analyzer.py
│   ├── reporter.py
│   └── stress_test.py
│
├── requirements.txt
└── README.md
```

---

# Stage 1 – Greedy Scheduling

### Strategy

Classes are sorted by student enrollment size in descending order.

Larger classes are scheduled first because they are more difficult to place due to room-capacity constraints.

### Process

1. Sort classes by number of students.
2. Search for the first available room and time slot.
3. Assign the class if constraints are satisfied.
4. Mark unscheduled classes if no feasible assignment exists.

### Benefit

Provides a fast baseline schedule and reduces the likelihood of large classes becoming impossible to place later.

### Time Complexity

```text
O(C × T × R)
```

Where:

* C = Number of Classes
* T = Number of Time Slots
* R = Number of Rooms

---

# Stage 2 – Conflict Graph and Welsh-Powell Coloring

### Strategy

A conflict graph is created where:

* Nodes represent classes.
* Edges represent scheduling conflicts.

Conflicts occur when:

* Two classes share the same professor.
* Two classes belong to the same student group.

### Welsh-Powell Algorithm

Classes are sorted according to the number of conflicts.

Time slots are assigned using graph coloring principles.

### Benefit

Ensures conflicting classes are never assigned to the same time slot.

### Time Complexity

```text
O(V²)
```

Where:

* V = Number of Classes

---

# Stage 3 – Dynamic Programming Room Optimization

### Objective

Minimize room-capacity waste after time slots have been assigned.

### DP State

```text
(class_index, used_room_mask)
```

Meaning:

```text
The first class_index classes have been assigned
using the rooms represented by used_room_mask.
```

### Recurrence

For each class:

1. Try every unused room.
2. Verify room capacity.
3. Compute wasted seats.
4. Select the assignment with minimum total waste.

### Benefit

Produces significantly better room utilization than the greedy baseline.

### Time Complexity

```text
O(C × 2^R × R)
```

---

# Stage 4 – Best-Effort Recursive Backtracking

### Objective

Recover classes that remain unscheduled after previous stages.

### Strategy

The algorithm recursively explores alternative room and time-slot assignments.

If a valid placement cannot be found:

* The class is marked as Unscheduled.
* A reason is recorded.
* Manual intervention is recommended.

### Benefit

Improves schedule completeness under tight constraints.

### Time Complexity

```text
O((T × R)^C)
```

Worst-case complexity.

---

# Conflict Report

The system produces a conflict report highlighting scheduling outcomes.

Example:

```text
Scheduled CS101 09:00 HALL1 Perfect Fit

Scheduled DB201 10:00 AUD1 Wasted 10 seats

Unscheduled AI301 N/A N/A
```

The report contains:

* Total classes
* Scheduled classes
* Unscheduled classes
* Capacity waste
* Manual intervention recommendations

---

# Manual Fix Log

In situations where the scheduler cannot place all classes automatically, the remaining conflicts are reported to a timetable administrator.

Possible manual resolutions include:

* Opening additional rooms.
* Creating new time slots.
* Assigning substitute professors.
* Moving low-priority courses.
* Increasing room availability.

This allows the final 1–2% of scheduling conflicts to be resolved manually.

---

# Validation System

The validator verifies that the generated schedule satisfies all constraints.

Checks include:

* Room double-booking
* Professor conflicts
* Student group conflicts

Example Output:

```text
Schedule Valid: True
Room Conflicts: 0
Professor Conflicts: 0
Student Group Conflicts: 0
```

---

# Conflict Analysis

The project compares scheduling quality before and after optimization.

Metrics:

* Greedy schedule conflicts
* Final schedule conflicts
* Conflict reduction

Example:

```text
Greedy Conflicts: 4
Final Schedule Conflicts: 0
```

---

# Schedule Quality Analysis

Additional decision-support metrics include:

* Total capacity waste
* Waste reduction
* Scheduling success rate
* Quality score

Example:

```text
Greedy Waste: 706
Optimized Waste: 671
Waste Improvement: 35
Scheduling Success Rate: 100%
Quality Score: 95.53 / 100
```

---

# Professor Workload Analysis

The system evaluates teaching workload distribution.

Metrics:

* Classes per professor
* Maximum workload
* Minimum workload
* Load difference

Example:

```text
Maximum Load: 3
Minimum Load: 2
Load Difference: 1
```

---

# Stress Test

A dedicated stress-testing dataset is included.

File:

```text
data/constraints_stress.json
```

Purpose:

* Limited rooms
* Limited time slots
* High conflict density

This dataset demonstrates the effectiveness of the backtracking recovery mechanism when complete scheduling is impossible.

---

# Running the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the main scheduler:

```bash
python src/main.py
```

Run the stress test:

```bash
python src/stress_test.py
```

---

# Results Generated

The system generates:

* Final Schedule
* Conflict Report
* Validation Report
* Schedule Quality Analysis
* Conflict Analysis
* Professor Workload Analysis

Output file:

```text
results/final_schedule.json
```

---

# Conclusion

The Campus Scheduler demonstrates how multiple algorithmic paradigms can be combined to solve a real-world university scheduling problem.

The system successfully integrates:

* Greedy Scheduling
* Graph Coloring
* Dynamic Programming
* Recursive Backtracking

to produce efficient, conflict-free timetables while supporting human decision-makers through analytics and conflict reporting.
