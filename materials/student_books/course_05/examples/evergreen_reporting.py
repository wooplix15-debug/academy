from datetime import datetime

ROWS = [
    ("EVG-JOB-1501", "open", None, False),
    ("EVG-JOB-1502", "completed", "2027-01-21T10:00:00Z", False),
    ("EVG-JOB-1503", "cancelled", None, True),
    ("EVG-JOB-1504", "completed", "2027-01-26T15:00:00Z", False),
    ("EVG-JOB-1505", "open", None, False),
]


def utc(text):
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def weekly_report(rows, version):
    opened = sum(
        not cancelled and state != "completed"
        for _, state, _, cancelled in rows
    )
    if version == "V1":
        completed = sum(state == "completed"
                        for _, state, _, _ in rows)
    else:
        start = utc("2027-01-25T00:00:00Z")
        end = utc("2027-02-01T00:00:00Z")
        completed = sum(
            timestamp is not None and start <= utc(timestamp) < end
            for _, _, timestamp, _ in rows
        )
    return {"open": opened, "completed": completed}


if __name__ == "__main__":
    print("V1:", weekly_report(ROWS, "V1"))
    print("V2:", weekly_report(ROWS, "V2"))
