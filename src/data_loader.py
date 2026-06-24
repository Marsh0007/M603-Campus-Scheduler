import json


def load_constraints(file_path):
    with open(file_path, "r") as file:
        return json.load(file)
    
def get_class_groups(class_id, student_groups):
    groups = []

    for group, class_list in student_groups.items():
        if class_id in class_list:
            groups.append(group)

    return groups