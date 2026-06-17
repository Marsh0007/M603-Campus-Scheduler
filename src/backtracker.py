def find_unscheduled_classes(schedule):
    return [
        item for item in schedule
        if item["status"] == "Unscheduled"
    ]


def get_class_groups(class_id, student_groups):
    groups = []

    for group, class_list in student_groups.items():
        if class_id in class_list:
            groups.append(group)

    return groups


def has_student_group_conflict(class_id, time_slot, schedule, student_groups):
    current_groups = get_class_groups(class_id, student_groups)

    for item in schedule:
        if item["status"] != "Scheduled":
            continue

        if item["time"] != time_slot:
            continue

        existing_groups = get_class_groups(item["class"], student_groups)

        for group in current_groups:
            if group in existing_groups:
                return True

    return False


def is_valid_assignment(class_item, room, time_slot, schedule, student_groups):
    class_id = class_item["id"]
    professor = class_item["professor"]
    students = class_item["students"]

    if room["capacity"] < students:
        return False

    for item in schedule:
        if item["status"] != "Scheduled":
            continue

        if item["time"] == time_slot and item["room"] == room["id"]:
            return False

        if item["time"] == time_slot and item["professor"] == professor:
            return False

    if has_student_group_conflict(class_id, time_slot, schedule, student_groups):
        return False

    return True


def count_scheduled(schedule):
    return len([
        item for item in schedule
        if item["status"] == "Scheduled"
    ])


def recursive_best_effort(
    classes,
    rooms,
    time_slots,
    student_groups,
    index,
    schedule,
    best_result
):
    if index == len(classes):
        scheduled_count = count_scheduled(schedule)

        if scheduled_count > best_result["scheduled_count"]:
            best_result["scheduled_count"] = scheduled_count
            best_result["schedule"] = [
                item.copy() for item in schedule
            ]

        return

    class_item = classes[index]
    placed_anywhere = False

    for time_slot in time_slots:
        for room in rooms:
            if is_valid_assignment(
                class_item,
                room,
                time_slot,
                schedule,
                student_groups
            ):
                placed_anywhere = True
                waste = room["capacity"] - class_item["students"]

                schedule.append({
                    "class": class_item["id"],
                    "students": class_item["students"],
                    "professor": class_item["professor"],
                    "time": time_slot,
                    "room": room["id"],
                    "wasted_seats": waste,
                    "status": "Scheduled"
                })

                recursive_best_effort(
                    classes,
                    rooms,
                    time_slots,
                    student_groups,
                    index + 1,
                    schedule,
                    best_result
                )

                schedule.pop()

    if not placed_anywhere:
        schedule.append({
            "class": class_item["id"],
            "students": class_item["students"],
            "professor": class_item["professor"],
            "time": "N/A",
            "room": "N/A",
            "wasted_seats": 0,
            "status": "Unscheduled",
            "reason": "No valid room/time slot found"
        })

        recursive_best_effort(
            classes,
            rooms,
            time_slots,
            student_groups,
            index + 1,
            schedule,
            best_result
        )

        schedule.pop()


def run_best_effort_backtracking(
    classes,
    rooms,
    time_slots,
    student_groups,
    initial_schedule=None
):
    sorted_classes = sorted(
        classes,
        key=lambda x: x["students"],
        reverse=True
    )

    if initial_schedule is None:
        initial_schedule = []

    starting_schedule = [
        item.copy() for item in initial_schedule
    ]

    best_result = {
        "scheduled_count": count_scheduled(starting_schedule),
        "schedule": [
            item.copy() for item in starting_schedule
        ]
    }

    recursive_best_effort(
        sorted_classes,
        rooms,
        time_slots,
        student_groups,
        0,
        starting_schedule,
        best_result
    )

    final_schedule = best_result["schedule"]

    scheduled_ids = {
        item["class"] for item in final_schedule
        if item["status"] == "Scheduled"
    }

    existing_ids = {
        item["class"] for item in final_schedule
    }

    for class_item in sorted_classes:
        if (
            class_item["id"] not in scheduled_ids
            and class_item["id"] not in existing_ids
        ):
            final_schedule.append({
                "class": class_item["id"],
                "students": class_item["students"],
                "professor": class_item["professor"],
                "time": "N/A",
                "room": "N/A",
                "wasted_seats": 0,
                "status": "Unscheduled",
                "reason": "No valid room/time slot found"
            })

    total_waste = sum(
        item["wasted_seats"] for item in final_schedule
        if item["status"] == "Scheduled"
    )

    success = all(
        item["status"] == "Scheduled"
        for item in final_schedule
    )

    return final_schedule, total_waste, success


def generate_conflict_report(final_schedule, total_waste):
    scheduled = [
        item for item in final_schedule
        if item["status"] == "Scheduled"
    ]

    unscheduled = [
        item for item in final_schedule
        if item["status"] == "Unscheduled"
    ]

    return {
        "total_classes": len(final_schedule),
        "scheduled_classes": len(scheduled),
        "unscheduled_classes": len(unscheduled),
        "total_capacity_waste": total_waste,
        "manual_intervention_required": len(unscheduled) > 0,
        "unscheduled_details": unscheduled
    }