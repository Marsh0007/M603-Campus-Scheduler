def analyze_professor_workload(final_schedule, data):
    professor_map = {}

    for course in data["classes"]:
        professor_map[course["id"]] = course["professor"]

    workload = {}

    for item in final_schedule:
        if item["status"] == "Scheduled":
            professor = professor_map[item["class"]]

            if professor not in workload:
                workload[professor] = 0

            workload[professor] += 1

    max_load = max(workload.values()) if workload else 0
    min_load = min(workload.values()) if workload else 0

    return {
        "professor_workload": workload,
        "max_load": max_load,
        "min_load": min_load,
        "load_difference": max_load - min_load
    }