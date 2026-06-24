import json
import os

from data_loader import load_constraints
from graph_engine import build_conflict_graph, welsh_powell_coloring
from optimizer import assign_rooms
from backtracker import generate_conflict_report, run_best_effort_backtracking


def print_schedule(title, schedule):
    print(f"\n===== {title} =====\n")

    for item in schedule:

        if item["status"] == "Scheduled":

            if item["wasted_seats"] == 0:
                fit_text = "Perfect Fit"
            else:
                fit_text = f"Wasted {item['wasted_seats']} seats"

            print(
                f"Scheduled {item['class']} "
                f"{item['time']} "
                f"{item['room']} "
                f"{fit_text}"
            )

        else:
            print(
                f"Unscheduled {item['class']} N/A N/A"
            )


def save_stress_results(
    final_schedule,
    conflict_report,
    file_path="results/stress_test_results.json"
):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    output = {
        "stress_test_schedule": final_schedule,
        "stress_test_conflict_report": conflict_report
    }

    with open(file_path, "w") as file:
        json.dump(output, file, indent=4)

    return file_path


def main():
    data = load_constraints("data/constraints_stress.json")

    conflict_graph = build_conflict_graph(data)
    time_assignment = welsh_powell_coloring(conflict_graph, data["time_slots"])

    print("\n===== STRESS TEST: GRAPH COLORING =====\n")

    for course, slot in time_assignment.items():
        print(f"{course} -> {slot}")

    final_schedule, total_waste = assign_rooms(time_assignment, data)

    print_schedule("STRESS TEST: STAGE 3 RESULT", final_schedule)

    scheduled_classes = [
        item for item in final_schedule
        if item["status"] == "Scheduled"
    ]

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
            data["student_groups"],
            initial_schedule=scheduled_classes
        )

        final_stress_schedule = backtracking_schedule
        final_stress_waste = backtracking_waste

        print_schedule(
            "STRESS TEST: STAGE 4 BACKTRACKING RESULT",
            final_stress_schedule
        )

        conflict_report = generate_conflict_report(
            final_stress_schedule,
            final_stress_waste
        )

    else:
        print("\nStage 4 not required.")

        final_stress_schedule = final_schedule
        final_stress_waste = total_waste

        conflict_report = generate_conflict_report(
            final_stress_schedule,
            final_stress_waste
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

    saved_file = save_stress_results(
        final_stress_schedule,
        conflict_report
    )

    print(f"\nStress test results saved to: {saved_file}")


if __name__ == "__main__":
    main()