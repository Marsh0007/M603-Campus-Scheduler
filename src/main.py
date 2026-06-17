from data_loader import load_constraints
from greedy_solver import generate_greedy_schedule
from graph_engine import build_conflict_graph, welsh_powell_coloring
from optimizer import assign_rooms
from backtracker import generate_conflict_report, run_best_effort_backtracking
from reporter import save_results
from quality_analyzer import analyze_schedule_quality
from professor_analyzer import analyze_professor_workload
from conflict_analyzer import count_schedule_conflicts
from validator import validate_schedule


def format_waste(item):
    if item["status"] == "Unscheduled":
        return ""

    if item["wasted_seats"] == 0:
        return "Perfect Fit"

    return f"Wasted {item['wasted_seats']} seats"


def print_schedule(title, schedule):
    print(f"\n===== {title} =====\n")

    for item in schedule:
        if item["status"] == "Scheduled":
            print(
                f"Scheduled {item['class']} "
                f"{item['time']} "
                f"{item['room']} "
                f"{format_waste(item)}"
            )
        else:
            print(
                f"Unscheduled {item['class']} "
                f"N/A N/A"
            )


def main():
    data = load_constraints("data/constraints.json")

    greedy_schedule = generate_greedy_schedule(data)
    print_schedule("STAGE 1: GREEDY SCHEDULE", greedy_schedule)

    greedy_conflict_analysis = count_schedule_conflicts(
        greedy_schedule,
        data
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

    print_schedule("STAGE 3: ROOM OPTIMIZATION", final_schedule)
    print(f"\nTotal Capacity Waste: {total_waste}")

    scheduled_classes = [
        item for item in final_schedule
        if item["status"] == "Scheduled"
    ]

    unscheduled_classes = [
        item for item in final_schedule
        if item["status"] == "Unscheduled"
    ]

    print("\n===== STAGE 4: BEST-EFFORT BACKTRACKING =====\n")

    if unscheduled_classes:
        print("Stage 4 activated: unresolved classes found after Stage 3.")

        unscheduled_ids = [
            item["class"]
            for item in unscheduled_classes
        ]

        unscheduled_class_objects = [
            course
            for course in data["classes"]
            if course["id"] in unscheduled_ids
        ]

        backtracking_schedule, backtracking_waste, backtracking_success = run_best_effort_backtracking(
            unscheduled_class_objects,
            data["rooms"],
            data["time_slots"],
            data["student_groups"],
            initial_schedule=scheduled_classes
        )

        final_schedule = backtracking_schedule

        total_waste = sum(
            item["wasted_seats"]
            for item in final_schedule
            if item["status"] == "Scheduled"
        )

        print_schedule(
            "STAGE 4: BACKTRACKING RESULT",
            backtracking_schedule
        )
    else:
        print("No unscheduled classes from Stage 3.")
        print("Backtracking not required for this dataset.")

    conflict_report = generate_conflict_report(
        final_schedule,
        total_waste
    )

    final_conflict_analysis = count_schedule_conflicts(
        final_schedule,
        data
    )

    validation_report = validate_schedule(
        final_schedule,
        data
    )

    print("\n===== STAGE 4: BEST-EFFORT CONFLICT REPORT =====\n")

    print(f"Total Classes: {conflict_report['total_classes']}")
    print(f"Scheduled Classes: {conflict_report['scheduled_classes']}")
    print(f"Unscheduled Classes: {conflict_report['unscheduled_classes']}")
    print(f"Total Capacity Waste: {conflict_report['total_capacity_waste']}")
    print(
        f"Manual Intervention Required: "
        f"{conflict_report['manual_intervention_required']}"
    )

    if conflict_report["unscheduled_details"]:
        print("\nManual Intervention Needed:")
        for item in conflict_report["unscheduled_details"]:
            print(
                f"{item['class']} could not be scheduled. "
                f"Reason: {item.get('reason', 'No feasible assignment found')}"
            )
    else:
        print("\nNo manual intervention needed. All classes were scheduled.")

    print("\n===== CONFLICT ANALYSIS =====\n")

    print(
        f"Greedy Conflicts: "
        f"{greedy_conflict_analysis['total_conflicts']}"
    )
    print(
        f"Final Schedule Conflicts: "
        f"{final_conflict_analysis['total_conflicts']}"
    )

    print("\n===== VALIDATION REPORT =====\n")

    print(f"Schedule Valid: {validation_report['is_valid']}")
    print(f"Room Conflicts: {validation_report['room_conflicts']}")
    print(f"Professor Conflicts: {validation_report['professor_conflicts']}")
    print(f"Student Group Conflicts: {validation_report['student_group_conflicts']}")

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
        professor_analysis,
        {
            "greedy_conflict_analysis": greedy_conflict_analysis,
            "final_conflict_analysis": final_conflict_analysis,
            "validation_report": validation_report
        }
    )

    print(f"\nResults saved to: {saved_file}")


if __name__ == "__main__":
    main()