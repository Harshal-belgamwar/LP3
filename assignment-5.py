
import re
import argparse
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

PATTERN = re.compile(
    r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) "
    r"([A-Z]+) user=(\S+) action=(\S+) ip=(\S+)$"
)

def parse_log(line):
    match = PATTERN.match(line.strip())
    if not match:
        return None

    timestamp, level, user, action, ip = match.groups()

    return {
        "time": datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"),
        "level": level,
        "user": user,
        "action": action,
        "ip": ip
    }


def correlate_events(events, threshold=3, window=5):
    failures = defaultdict(list)
    duration = timedelta(minutes=window)

    for event in sorted(events, key=lambda e: e["time"]):
        if event["action"] != "login_failed":
            continue

        ip = event["ip"]
        now = event["time"]

        failures[ip] = [
            t for t in failures[ip]
            if now - t <= duration
        ]
        failures[ip].append(now)

        if len(failures[ip]) == threshold:
            print(
                f"[ALERT] Suspicious activity from {ip}: "
                f"{threshold} failed logins within {window} minutes"
            )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("logfile")
    args = parser.parse_args()

    events = []

    with Path(args.logfile).open(
        encoding="utf-8", errors="replace"
    ) as file:
        for line in file:
            event = parse_log(line)
            if event:
                events.append(event)

    print("Total events captured:", len(events))
    correlate_events(events)


if __name__ == "__main__":
    main()
