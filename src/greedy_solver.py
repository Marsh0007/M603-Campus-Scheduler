def get_class_groups(class_id, student_groups):
    groups = []

    for group, class_list in student_groups.items():
        if class_id in class_list:
            groups.append(group)

    return groups


def has_conflict(slot, course, course_groups, professor_busy, group_busy):
    professor = course["professor"]

    if professor in professor_busy.get(slot, set()):
        return True

    for group in course_groups:
        if group in group_busy.get(slot, set()):
            return True

    return False


def generate_greedy_schedule(data):
    classes = sorted(
        data["classes"],
        key=lambda x: x["students"],
        reverse=True
    )

    rooms = data["rooms"]
    time_slots = data["time_slots"]
    student_groups = data["student_groups"]

    schedule = []

    occupied = set()
    professor_busy = {}
    group_busy = {}

    for course in classes:
        scheduled = False
        course_groups = get_class_groups(course["id"], student_groups)

        for slot in time_slots:
            for room in rooms:

                if room["capacity"] < course["students"]:
                    continue

                key = (slot, room["id"])

                if key in occupied:
                    continue

                if has_conflict(slot, course, course_groups, professor_busy, group_busy):
                    continue

                occupied.add(key)

                professor_busy.setdefault(slot, set()).add(course["professor"])

                for group in course_groups:
                    group_busy.setdefault(slot, set()).add(group)

                wasted_seats = room["capacity"] - course["students"]

                schedule.append({
                    "class": course["id"],
                    "students": course["students"],
                    "professor": course["professor"],
                    "time": slot,
                    "room": room["id"],
                    "wasted_seats": wasted_seats,
                    "status": "Scheduled"
                })

                scheduled = True
                break

            if scheduled:
                break

        if not scheduled:
            schedule.append({
                "class": course["id"],
                "students": course["students"],
                "professor": course["professor"],
                "time": "N/A",
                "room": "N/A",
                "wasted_seats": 0,
                "status": "Unscheduled"
            })

    return schedule