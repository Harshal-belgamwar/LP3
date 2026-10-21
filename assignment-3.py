
from collections import defaultdict, deque
from datetime import datetime, timedelta

MAX_FAILURES = 5
TIME_WINDOW = timedelta(minutes=2)

# Store failed attempts and blocked devices
failed_attempts = defaultdict(deque)
blocked_devices = set()
authorized_devices = {
    "AA:BB:CC:DD:EE:01"
}


def detect_intrusion(mac, success):
    now = datetime.now()
    mac = mac.upper()

    if mac in blocked_devices:
        print(f"[BLOCKED] Device {mac} is prohibited.")
        return

    if success:
        failed_attempts[mac].clear()
        print(f"[SUCCESS] Authentication accepted for {mac}")
        return

    attempts = failed_attempts[mac]

    # Remove failures older than the time window
    while attempts and now - attempts[0] > TIME_WINDOW:
        attempts.popleft()

    attempts.append(now)

    print(f"[ALERT] Failed authentication from {mac}")
    print(f"Failed attempts: {len(attempts)}")

    if len(attempts) >= MAX_FAILURES:
        blocked_devices.add(mac)
        print(f"[INTRUSION DETECTED] {mac}")
        print("[ACTION] Device added to block list.")


def check_printer_access(mac):
    mac = mac.upper()

    if mac in blocked_devices:
        print("PRINTER ACCESS DENIED: Device is blocked.")
    elif mac in authorized_devices:
        print("PRINTER ACCESS GRANTED.")
    else:
        print("PRINTER ACCESS DENIED: Device is not authorized.")


def main():
    attacker = "11:22:33:44:55:66"
    trusted = "AA:BB:CC:DD:EE:01"

    print("=== Wi-Fi Intrusion Detection System ===")

    # Simulate repeated failed authentication
    for attempt in range(1, 6):
        print(f"\nAttempt {attempt}")
        detect_intrusion(attacker, success=False)

    print("\n=== Printer Access Test ===")
    check_printer_access(attacker)
    check_printer_access(trusted)


if __name__ == "__main__":
    main()
