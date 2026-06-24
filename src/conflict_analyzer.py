from data_loader import get_class_groups

def count_schedule_conflicts(schedule, data):
    professor_conflicts = 0
    student_group_conflicts = 0
    conflict_details = []

    student_groups = data["student_groups"]

    scheduled_items = [
        item for item in schedule
        if item["status"] == "Scheduled"
    ]

    for i in range(len(scheduled_items)):
        for j in range(i + 1, len(scheduled_items)):
            first = scheduled_items[i]
            second = scheduled_items[j]

            if first["time"] != second["time"]:
                continue

            if first["professor"] == second["professor"]:
                professor_conflicts += 1
                conflict_details.append({
                    "type": "Professor Conflict",
                    "time": first["time"],
                    "class_1": first["class"],
                    "class_2": second["class"],
                    "professor": first["professor"]
                })

            first_groups = get_class_groups(first["class"], student_groups)
            second_groups = get_class_groups(second["class"], student_groups)

            common_groups = [
                group for group in first_groups
                if group in second_groups
            ]

            if common_groups:
                student_group_conflicts += 1
                conflict_details.append({
                    "type": "Student Group Conflict",
                    "time": first["time"],
                    "class_1": first["class"],
                    "class_2": second["class"],
                    "student_groups": common_groups
                })

    total_conflicts = professor_conflicts + student_group_conflicts

    return {
        "professor_conflicts": professor_conflicts,
        "student_group_conflicts": student_group_conflicts,
        "total_conflicts": total_conflicts,
        "conflict_details": conflict_details
    }