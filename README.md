# Campus Scheduler and Decision Support System

Advanced Algorithms (M603) Project

## Project Overview

The Campus Scheduler and Decision Support System addresses the university timetable generation problem. The objective is to create a conflict-free schedule while minimizing room-capacity waste and providing decision support when a complete schedule is not possible.

The system considers:

* Professor availability conflicts
* Student group conflicts
* Room capacity constraints
* Room utilization efficiency
* Schedule quality metrics
* Professor workload balancing

The project follows a multi-stage optimization pipeline consisting of Greedy Scheduling, Graph Coloring, Dynamic Programming, and Recursive Backtracking.

---

## Problem Definition

Universities must schedule many classes across limited rooms and time slots.

The scheduling system must satisfy the following hard constraints:

1. A professor cannot teach two classes simultaneously.
2. A student group cannot attend two classes simultaneously.
3. A room cannot host more than one class at the same time.
4. Room capacity must be sufficient for enrolled students.

The optimization objective is to minimize wasted room capacity while satisfying all constraints.

---

## Algorithm Design

### Stage 1 – Greedy Scheduling

#### Algorithm

Classes are sorted in descending order by enrollment size.

Larger classes are scheduled first because they are harder to place into available rooms.

#### Justification

Greedy algorithms provide fast baseline solutions with low computational cost.

#### Complexity

Time Complexity: O(C × R × T)

Space Complexity: O(C)

Where:

* C = number of classes
* R = number of rooms
* T = number of time slots

---

### Stage 2 – Graph Theory

#### Conflict Graph Construction

Each class is represented as a node.

An edge exists between two classes if:

* They share the same professor, or
* They belong to the same student group.

#### Graph Coloring

Welsh-Powell Graph Coloring assigns time slots to classes.

Classes connected by an edge cannot receive the same color (time slot).

#### Justification

Graph coloring naturally models scheduling conflicts and guarantees conflict-free time assignments.

#### Complexity

Time Complexity: O(V²)

Space Complexity: O(V + E)

Where:

* V = number of classes
* E = number of conflict edges

---

### Stage 3 – Dynamic Programming

#### Objective

Minimize total room-capacity waste while respecting fixed time-slot assignments.

#### DP State

(class_index, used_room_mask)

#### Justification

Dynamic Programming avoids evaluating every possible room allocation combination by storing previously solved states.

#### Complexity

Time Complexity: O(C × 2^R)

Space Complexity: O(C × 2^R)

---

### Stage 4 – Recursive Backtracking

#### Objective

Handle situations where previous stages cannot generate a complete schedule.

#### Strategy

1. Attempt assignment.
2. Check constraints.
3. Continue recursively.
4. If a dead end is reached:

   * Undo the previous assignment.
   * Try an alternative assignment.

#### Pruning Strategy

The search is reduced by:

* Scheduling larger classes first.
* Rejecting room-capacity violations immediately.
* Rejecting professor conflicts immediately.
* Rejecting student-group conflicts immediately.

#### Justification

Backtracking provides a best-effort solution when a complete schedule may not exist.

---

## Conflict Report

When all classes cannot be scheduled, the system generates a conflict report.

Example:

Scheduled: CS101 | 09:00 | HALL1

Scheduled: MATH101 | 10:00 | AUD2

Unscheduled: WEB102

Reason:
No valid room and time-slot combination available after recursive backtracking.

---

## Manual Fix Log

If unscheduled classes remain, a university scheduler can:

1. Add additional rooms.
2. Create additional time slots.
3. Increase room capacities.
4. Split large classes into multiple sessions.

The software highlights these unresolved conflicts for manual review.

---

## Project Structure

M603_CampusScheduler/

├── data/

├── src/

├── results/

├── README.md

└── requirements.txt

---

## Running the Project

```bash
python src/main.py
```

---

## Dataset

Current dataset contains:

* 30 Classes
* 10 Rooms
* 12 Professors
* 8 Student Groups
* Multiple realistic scheduling conflicts
* Variable class sizes

---

## Additional Features

### Schedule Quality Analysis

Measures:

* Scheduling Success Rate
* Total Capacity Waste
* Average Waste Per Class
* Schedule Quality Score

### Professor Workload Analysis

Measures:

* Classes per Professor
* Maximum Workload
* Minimum Workload
* Workload Difference

---

## Technologies

* Python 3
* JSON
* Greedy Algorithms
* Graph Algorithms
* Dynamic Programming
* Recursive Backtracking

---

## Module

M603 Advanced Algorithms

GISMA University of Applied Sciences
