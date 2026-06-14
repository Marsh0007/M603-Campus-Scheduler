def find_unscheduled_classes(schedule):
    return [
        item for item in schedule
        if item["status"] == "Unscheduled"
    ]


def has_student_group_conflict(class_id, time_slot, schedule, student_groups):
    """
    Checks whether the class has a student group conflict at the given time slot.
    If two classes belong to the same student group, they cannot be scheduled
    at the same time.
    """
    for group_classes in student_groups.values():
        if class_id in group_classes:
            for item in schedule:
                if (
                    item["status"] == "Scheduled"
                    and item["time"] == time_slot
                    and item["class_id"] in group_classes
                ):
                    return True
    return False


def is_valid_assignment(class_item, room, time_slot, schedule, student_groups):
    """
    Checks whether assigning a class to a room and time slot is valid.
    """
    class_id = class_item["id"]
    professor = class_item["professor"]
    students = class_item["students"]

    # Room must be large enough
    if room["capacity"] < students:
        return False

    for item in schedule:
        if item["status"] != "Scheduled":
            continue

        # Room cannot be double-booked
        if item["time"] == time_slot and item["room"] == room["id"]:
            return False

        # Professor cannot teach two classes at the same time
        if item["time"] == time_slot and item.get("professor") == professor:
            return False

    # Student group cannot attend two classes at the same time
    if has_student_group_conflict(class_id, time_slot, schedule, student_groups):
        return False

    return True


def recursive_backtracking(classes, rooms, time_slots, student_groups, schedule, index=0):
    """
    Recursive backtracking scheduler.

    It tries to assign each class to a valid room and time slot.
    If a later class cannot be scheduled, the algorithm backtracks by
    removing the previous assignment and trying another option.
    """
    if index == len(classes):
        return True

    class_item = classes[index]

    # Try every time slot and room combination
    for time_slot in time_slots:
        for room in rooms:
            if is_valid_assignment(class_item, room, time_slot, schedule, student_groups):
                waste = room["capacity"] - class_item["students"]

                schedule.append({
                    "class_id": class_item["id"],
                    "time": time_slot,
                    "room": room["id"],
                    "waste": waste,
                    "status": "Scheduled",
                    "professor": class_item["professor"]
                })

                # Move to next class
                if recursive_backtracking(classes, rooms, time_slots, student_groups, schedule, index + 1):
                    return True

                # Undo assignment if it leads to failure
                schedule.pop()

    return False


def run_best_effort_backtracking(classes, rooms, time_slots, student_groups):
    """
    Runs recursive backtracking. If a complete schedule is impossible,
    it keeps a best-effort partial schedule and marks remaining classes
    as unscheduled.
    """
    schedule = []

    # Sort large classes first because they are harder to place
    sorted_classes = sorted(classes, key=lambda x: x["students"], reverse=True)

    success = recursive_backtracking(
        sorted_classes,
        rooms,
        time_slots,
        student_groups,
        schedule
    )

    scheduled_ids = {item["class_id"] for item in schedule}

    for class_item in sorted_classes:
        if class_item["id"] not in scheduled_ids:
            schedule.append({
                "class_id": class_item["id"],
                "time": "N/A",
                "room": "N/A",
                "waste": "N/A",
                "status": "Unscheduled",
                "professor": class_item["professor"],
                "reason": "No valid room/time slot found after recursive backtracking"
            })

    total_waste = sum(
        item["waste"] for item in schedule
        if item["status"] == "Scheduled"
    )

    return schedule, total_waste, success


def generate_conflict_report(final_schedule, total_waste):
    scheduled = [
        item for item in final_schedule
        if item["status"] == "Scheduled"
    ]

    unscheduled = [
        item for item in final_schedule
        if item["status"] == "Unscheduled"
    ]

    report = {
        "total_classes": len(final_schedule),
        "scheduled_classes": len(scheduled),
        "unscheduled_classes": len(unscheduled),
        "total_capacity_waste": total_waste,
        "unscheduled_details": unscheduled
    }

    return report