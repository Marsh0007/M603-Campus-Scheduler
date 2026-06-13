def analyze_schedule_quality(
    greedy_schedule,
    optimized_schedule
):
    greedy_waste = sum(
        item["wasted_seats"]
        for item in greedy_schedule
        if item["status"] == "Scheduled"
    )

    optimized_waste = sum(
        item["wasted_seats"]
        for item in optimized_schedule
        if item["status"] == "Scheduled"
    )

    scheduled = [
        item
        for item in optimized_schedule
        if item["status"] == "Scheduled"
    ]

    unscheduled = [
        item
        for item in optimized_schedule
        if item["status"] == "Unscheduled"
    ]

    total_classes = len(optimized_schedule)

    scheduling_success_rate = (
        len(scheduled) / total_classes
    ) * 100

    average_waste = (
        optimized_waste / len(scheduled)
        if scheduled
        else 0
    )

    waste_improvement = greedy_waste - optimized_waste

    quality_score = 100

    quality_score -= len(unscheduled) * 10
    quality_score -= average_waste * 0.2

    if quality_score < 0:
        quality_score = 0

    return {
        "greedy_waste": greedy_waste,
        "optimized_waste": optimized_waste,
        "waste_improvement": waste_improvement,
        "scheduling_success_rate": round(
            scheduling_success_rate,
            2
        ),
        "average_waste_per_class": round(
            average_waste,
            2
        ),
        "quality_score": round(
            quality_score,
            2
        )
    }