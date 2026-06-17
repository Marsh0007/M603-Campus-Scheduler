from data_loader import load_constraints
from graph_engine import build_conflict_graph, welsh_powell_coloring
from optimizer import assign_rooms
from backtracker import generate_conflict_report, run_best_effort_backtracking


def print_schedule(title, schedule):
    print(f"\n===== {title} =====\n")

    for item in schedule:
        print(
            f"{item['class']} | "
            f"{item['time']} | "
            f"{item['room']} | "
            f"Waste: {item['wasted_seats']} | "
            f"{item['status']}"
        )


def main():
    data = load_constraints("data/constraints_stress.json")

    conflict_graph = build_conflict_graph(data)
    time_assignment = welsh_powell_coloring(conflict_graph, data["time_slots"])

    print("\n===== STRESS TEST: GRAPH COLORING =====\n")

    for course, slot in time_assignment.items():
        print(f"{course} -> {slot}")

    final_schedule, total_waste = assign_rooms(time_assignment, data)

    print_schedule("STRESS TEST: STAGE 3 RESULT", final_schedule)

    unscheduled_classes = [
        course
        for course in data["classes"]
        if any(
            item["class"] == course["id"]
            and item["status"] == "Unscheduled"
            for item in final_schedule
        )
    ]

    if unscheduled_classes:
        print("\nStage 4 activated: unscheduled classes found.\n")

        backtracking_schedule, backtracking_waste, success = run_best_effort_backtracking(
            unscheduled_classes,
            data["rooms"],
            data["time_slots"],
            data["student_groups"]
        )

        print_schedule(
            "STRESS TEST: STAGE 4 BACKTRACKING RESULT",
            backtracking_schedule
        )

        conflict_report = generate_conflict_report(
            backtracking_schedule,
            backtracking_waste
        )

    else:
        print("\nStage 4 not required.")

        conflict_report = generate_conflict_report(
            final_schedule,
            total_waste
        )

    print("\n===== STRESS TEST: CONFLICT REPORT =====\n")
    print(f"Total Classes Checked: {conflict_report['total_classes']}")
    print(f"Scheduled Classes: {conflict_report['scheduled_classes']}")
    print(f"Unscheduled Classes: {conflict_report['unscheduled_classes']}")
    print(f"Manual Intervention Required: {conflict_report['manual_intervention_required']}")

    if conflict_report["unscheduled_details"]:
        print("\nManual Intervention Needed:")
        for item in conflict_report["unscheduled_details"]:
            print(
                f"{item['class']} could not be scheduled. "
                f"Reason: {item.get('reason', 'No feasible assignment found')}"
            )


if __name__ == "__main__":
    main()