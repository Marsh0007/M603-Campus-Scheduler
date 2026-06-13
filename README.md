# Campus Scheduler and Decision Support System

Advanced Algorithms (M603) Project

## Overview

This project solves the university scheduling problem by generating a conflict-free timetable while minimizing room-capacity waste.

The system handles:

* Professor conflicts
* Student group conflicts
* Room allocation
* Capacity optimization
* Schedule quality analysis
* Professor workload analysis

---

## Algorithms Implemented

### Stage 1 - Greedy Scheduling

* Sort classes by enrollment size
* Assign to first available room and time slot

### Stage 2 - Graph Theory

* Conflict Graph Construction
* Welsh-Powell Graph Coloring

### Stage 3 - Dynamic Programming

* Room allocation optimization
* Capacity waste minimization

### Stage 4 - Best-Effort Scheduling

* Conflict reporting
* Manual intervention recommendations

---

## Project Structure

```text
M603_CampusScheduler/
│
├── data/
├── src/
├── results/
├── README.md
└── requirements.txt
```

---

## Running the Project

```bash
python src/main.py
```

---

## Generated Output

The system generates:

* Final Schedule
* Conflict Report
* Schedule Quality Analysis
* Professor Workload Analysis

Results are saved to:

```text
results/final_schedule.json
```

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

## 🛠 Technologies

* Python 3
* JSON
* Dynamic Programming
* Graph Algorithms
* Greedy Algorithms
* Backtracking Concepts

---

## Module

M603 Advanced Algorithms
GISMA University of Applied Sciences
