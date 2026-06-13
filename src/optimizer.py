def assign_rooms(time_assignment, data):
    rooms = data["rooms"]

    classes_lookup = {
        course["id"]: course
        for course in data["classes"]
    }

    final_schedule = []
    total_waste = 0

    for slot in data["time_slots"]:
        slot_classes = [
            course_id
            for course_id, assigned_slot in time_assignment.items()
            if assigned_slot == slot
        ]

        slot_schedule, slot_waste = optimize_rooms_for_slot(
            slot,
            slot_classes,
            rooms,
            classes_lookup
        )

        final_schedule.extend(slot_schedule)
        total_waste += slot_waste

    return final_schedule, total_waste


def optimize_rooms_for_slot(slot, slot_classes, rooms, classes_lookup):
    number_of_classes = len(slot_classes)

    if number_of_classes == 0:
        return [], 0

    # dp stores the best known state:
    # key = (class_index, used_room_mask)
    # value = (minimum_waste, assignment_list)
    dp = {
        (0, 0): (0, [])
    }

    for class_index in range(number_of_classes):
        course_id = slot_classes[class_index]
        course = classes_lookup[course_id]

        next_dp = {}

        for (current_index, used_mask), (current_waste, assignments) in dp.items():
            for room_index, room in enumerate(rooms):
                room_already_used = used_mask & (1 << room_index)

                if room_already_used:
                    continue

                if room["capacity"] < course["students"]:
                    continue

                new_mask = used_mask | (1 << room_index)
                wasted_seats = room["capacity"] - course["students"]
                new_waste = current_waste + wasted_seats

                new_assignment = assignments + [
                    {
                        "class": course_id,
                        "students": course["students"],
                        "time": slot,
                        "room": room["id"],
                        "wasted_seats": wasted_seats,
                        "status": "Scheduled"
                    }
                ]

                state_key = (class_index + 1, new_mask)

                if (
                    state_key not in next_dp
                    or new_waste < next_dp[state_key][0]
                ):
                    next_dp[state_key] = (new_waste, new_assignment)

        dp = next_dp

        if not dp:
            return mark_slot_as_unscheduled(
                slot,
                slot_classes,
                classes_lookup
            ), 0

    best_waste = float("inf")
    best_assignment = []

    for (class_index, used_mask), (waste, assignment) in dp.items():
        if class_index == number_of_classes and waste < best_waste:
            best_waste = waste
            best_assignment = assignment

    return best_assignment, best_waste


def mark_slot_as_unscheduled(slot, slot_classes, classes_lookup):
    unscheduled = []

    for course_id in slot_classes:
        course = classes_lookup[course_id]

        unscheduled.append({
            "class": course_id,
            "students": course["students"],
            "time": slot,
            "room": "N/A",
            "wasted_seats": 0,
            "status": "Unscheduled"
        })

    return unscheduled