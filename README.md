# M603 Campus Scheduler

**Advanced Algorithms (M603) – Individual Project**

A timetable scheduling system for the university which comprises of four algorithimic stages to generate conflict free schedules while minimizing room capacity waste as much as possible.

---

## Project Structure

```
M603_CampusScheduler/
├── data/
│   ├── constraints.json          # Main dataset
│   └── constraints_stress.json   # Stress test dataset
├── results/
│   └── final_schedule.json
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
├── requirements.txt
└── README.md
```

---

## How to Run

```bash
pip install -r requirements.txt

# Main dataset
python src/main.py

# Stress test
python src/stress_test.py
```

---

## Algorithm Justification

| Stage | Algorithm | Complexity | Justification |
|-------|-----------|------------|---------------|
| 1 | Greedy Scheduling | O(C × T × R) | Fast baseline; linear per class so it scales to thousands of classes instantly |
| 2 | Welsh-Powell Graph Coloring | O(V²) | Quadratic on class count, acceptable since V ≤ 300 in realistic university scenarios |
| 3 | Bitmask Dynamic Programming | O(C × 2^R × R) | Exponential on rooms per slot, kept tractable by applying DP one time slot at a time with a small room set |
| 4 | Recursive Backtracking | O((T × R)^C) worst case | Used only for residual unscheduled classes; pruning limits explored branches significantly |

*C = classes, T = time slots, R = rooms per slot, V = class nodes*

---

## Stage Descriptions

**Stage 1 – Greedy Baseline (`greedy_solver.py`)**  
Classes are organized by enrollment (lowest to highest). Larger classes are given priority because they need larger rooms; if large classes are scheduled first, only small rooms will be available. Professor and student-group constraints are used to assign each class to the first (room, time slot) pair that meets both constraints.

**Stage 2 – Conflict Graph & Welsh-Powell Coloring (`graph_engine.py`)**  
A conflict graph is constructed with nodes representing classes and edges connect any two classes that are taught by a common professor or a common group of students. A coloring of the process nodes that satisfies Welsh-Powell is obtained by coloring the nodes in decreasing degree order, so that no two nodes in the same class compete for the same time slot. This prevents the root cause of conflicts even prior to allocation of rooms.

**Stage 3 – Dynamic Programming Room Optimizer (`optimizer.py`)**  
With time slots fixed by Stage 2, a bitmask DP assigns rooms within each slot to minimise wasted seat capacity.  
- **State:** `(class_index, used_room_mask)` — classes processed so far and which rooms are occupied  
- **Recurrence:** For each unassigned class, try every feasible unused room, compute wasted seats, and retain the assignment with the lowest cumulative waste  
- **Advantage over brute force:** Instead of evaluating all room permutations (R! per slot), the DP reuses subproblem solutions, reducing the search space from factorial to O(C × 2^R × R)

**Stage 4 – Best-Effort Backtracking (`backtracker.py`)**  
A recursive search tries all other possible (slot, room) assignments for the class to be placed which is not yet assigned. If there is no valid placement to be found, the algorithm backtracks and marks the class as unscheduled with a reason. The search keeps the best partial solution that it finds — the assignment with maximum number of scheduled classes. 
**Pruning strategy:** Infeasible branches (capacity violations, professor or student-group conflicts) are detected before recursion, avoiding expansion of invalid subtrees.

---

## Conflict Report

The system produces a per-class scheduling outcome:

```
Scheduled   CS101    09:00   HALL1   Perfect Fit
Scheduled   DB201    10:00   AUD1    Wasted 10 seats
Unscheduled AI301    N/A     N/A     No valid slot — professor conflict
```

Summary metrics include total scheduled, total unscheduled, capacity waste, and validation status.

---

## Manual Fix Log

When the scheduler cannot place all classes automatically, a conflict report identifies each unscheduled class and the reason for failure. A timetable administrator can resolve these cases by:

- Opening an additional room or time slot
- Assigning a substitute professor
- Splitting an oversized class into two sections
- Deferring low-priority courses to the following semester

This workflow handles the residual 1 to 2% of conflicts that automated scheduling cannot resolve under strict constraints.

---

## Sample Results

**Main dataset (30 classes):**
```
Scheduled:       30 / 30
Conflicts:       0
Validation:      Passed
Greedy Waste:    706 seats
Optimized Waste: 671 seats
Waste Reduction: 35 seats
Quality Score:   95.53 / 100
```

**Stress test:**
```
Stage 4 activated:    Yes
Classes recovered:    3
Unscheduled:          1 (manual intervention required)
```

---

## Validation

The validator confirms the final schedule satisfies all hard constraints:

```
Room Conflicts:          0
Professor Conflicts:     0
Student Group Conflicts: 0
Schedule Valid:          True
```
