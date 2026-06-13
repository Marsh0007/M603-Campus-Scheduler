def generate_greedy_schedule(data):
    classes = sorted(
        data["classes"],
        key=lambda x: x["students"],
        reverse=True
    )

    rooms = data["rooms"]
    time_slots = data["time_slots"]

    schedule = []
    occupied = set()

    for course in classes:
        scheduled = False

        for slot in time_slots:
            for room in rooms:

                if room["capacity"] < course["students"]:
                    continue

                key = (slot, room["id"])

                if key not in occupied:
                    occupied.add(key)

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