def build_conflict_graph(data):
    classes = data["classes"]
    student_groups = data["student_groups"]

    graph = {course["id"]: set() for course in classes}

    # Professor conflicts
    for i in range(len(classes)):
        for j in range(i + 1, len(classes)):
            class_a = classes[i]
            class_b = classes[j]

            if class_a["professor"] == class_b["professor"]:
                graph[class_a["id"]].add(class_b["id"])
                graph[class_b["id"]].add(class_a["id"])

    # Student group conflicts
    for group_classes in student_groups.values():
        for i in range(len(group_classes)):
            for j in range(i + 1, len(group_classes)):
                class_a = group_classes[i]
                class_b = group_classes[j]

                graph[class_a].add(class_b)
                graph[class_b].add(class_a)

    return graph


def welsh_powell_coloring(graph, time_slots):
    # Sort classes by number of conflicts, highest first
    sorted_classes = sorted(
        graph.keys(),
        key=lambda course: len(graph[course]),
        reverse=True
    )

    color_assignment = {}

    for course in sorted_classes:
        used_slots = set()

        for neighbor in graph[course]:
            if neighbor in color_assignment:
                used_slots.add(color_assignment[neighbor])

        assigned = False

        for slot in time_slots:
            if slot not in used_slots:
                color_assignment[course] = slot
                assigned = True
                break

        if not assigned:
            color_assignment[course] = "N/A"

    return color_assignment