from data_loader import load_constraints
from greedy_solver import generate_greedy_schedule
from graph_engine import build_conflict_graph, welsh_powell_coloring
from optimizer import assign_rooms
from backtracker import generate_conflict_report
from reporter import save_results
from quality_analyzer import analyze_schedule_quality
from professor_analyzer import analyze_professor_workload


def main():
    data = load_constraints("data/constraints.json")

    greedy_schedule = generate_greedy_schedule(data)

    print("\n===== STAGE 1: GREEDY SCHEDULE =====\n")

    for item in greedy_schedule:
        print(
            f"{item['class']} | "
            f"{item['time']} | "
            f"{item['room']} | "
            f"Waste: {item['wasted_seats']} | "
            f"{item['status']}"
        )

    conflict_graph = build_conflict_graph(data)
    time_assignment = welsh_powell_coloring(conflict_graph, data["time_slots"])

    print("\n===== STAGE 2: CONFLICT GRAPH =====\n")

    for course, conflicts in conflict_graph.items():
        print(f"{course} conflicts with: {list(conflicts)}")

    print("\n===== STAGE 2: GRAPH COLORING TIME SLOTS =====\n")

    for course, slot in time_assignment.items():
        print(f"{course} -> {slot}")

    final_schedule, total_waste = assign_rooms(time_assignment, data)

    print("\n===== STAGE 3: ROOM OPTIMIZATION =====\n")

    for item in final_schedule:
        print(
            f"{item['class']} | "
            f"{item['time']} | "
            f"{item['room']} | "
            f"Waste: {item['wasted_seats']} | "
            f"{item['status']}"
        )

    print(f"\nTotal Capacity Waste: {total_waste}")

    conflict_report = generate_conflict_report(final_schedule, total_waste)

    print("\n===== STAGE 4: BEST-EFFORT CONFLICT REPORT =====\n")

    print(f"Total Classes: {conflict_report['total_classes']}")
    print(f"Scheduled Classes: {conflict_report['scheduled_classes']}")
    print(f"Unscheduled Classes: {conflict_report['unscheduled_classes']}")
    print(f"Total Capacity Waste: {conflict_report['total_capacity_waste']}")

    if conflict_report["unscheduled_details"]:
        print("\nManual Intervention Needed:")
        for item in conflict_report["unscheduled_details"]:
            print(f"{item['class']} could not be scheduled.")
    else:
        print("\nNo manual intervention needed. All classes were scheduled.")

    quality_analysis = analyze_schedule_quality(
        greedy_schedule,
        final_schedule
    )

    print("\n===== UNIQUE FEATURE: SCHEDULE QUALITY ANALYSIS =====\n")

    print(f"Greedy Waste: {quality_analysis['greedy_waste']}")
    print(f"Optimized Waste: {quality_analysis['optimized_waste']}")

    print(
        f"Waste Difference After Conflict Resolution: "
        f"{quality_analysis['waste_improvement']}"
    )

    print(
        f"Scheduling Success Rate: "
        f"{quality_analysis['scheduling_success_rate']}%"
    )

    print(
        f"Average Waste Per Class: "
        f"{quality_analysis['average_waste_per_class']}"
    )

    print(
        f"Schedule Quality Score: "
        f"{quality_analysis['quality_score']}/100"
    )

    # PROFESSOR WORKLOAD ANALYSIS
    professor_analysis = analyze_professor_workload(
        final_schedule,
        data
    )

    print("\n===== UNIQUE FEATURE: PROFESSOR WORKLOAD ANALYSIS =====\n")

    for professor, count in professor_analysis["professor_workload"].items():
        print(f"{professor}: {count} classes")

    print(f"\nMaximum Load: {professor_analysis['max_load']}")
    print(f"Minimum Load: {professor_analysis['min_load']}")
    print(
        f"Workload Difference: "
        f"{professor_analysis['load_difference']}"
    )

    saved_file = save_results(
    final_schedule,
    conflict_report,
    quality_analysis,
    professor_analysis
    )

    print(f"\nResults saved to: {saved_file}")


if __name__ == "__main__":
    main()