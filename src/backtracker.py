def find_unscheduled_classes(schedule):
    return [
        item for item in schedule
        if item["status"] == "Unscheduled"
    ]


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