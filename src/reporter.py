import json
import os


def save_results(
    final_schedule,
    conflict_report,
    quality_analysis,
    professor_analysis,
    file_path="results/final_schedule.json"
):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    output = {
        "final_schedule": final_schedule,
        "conflict_report": conflict_report,
        "quality_analysis": quality_analysis,
        "professor_analysis": professor_analysis
    }

    with open(file_path, "w") as file:
        json.dump(output, file, indent=4)

    return file_path