"""Lab 7 - Fixed parking_fee.py (hardened against invalid input).

Name: Dhanush S S | SRN: PES1UG24AM082 | Section: B

Every function now returns None for input it cannot handle, instead of
crashing or returning a wrong value.
"""
import re

RATES = {"bike": 10, "car": 30, "truck": 60}

# HH:MM-HH:MM with ASCII digits only, spaces allowed around the parts.
TIME_RANGE = re.compile(r"\s*([0-9]{1,2}):([0-9]{2})\s*-\s*([0-9]{1,2}):([0-9]{2})\s*")

# Indian-style plate: 2 letters, 2 digits, 2 letters, 4 digits (e.g. KA01AB1234).
PLATE = re.compile(r"[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}")


def _to_minutes(hours, mins):
    """Convert 'HH', 'MM' strings to minutes since midnight, or None."""
    h, m = int(hours), int(mins)
    if not (0 <= h <= 23 and 0 <= m <= 59):
        return None
    return h * 60 + m


def minutes_parked(times):
    """Minutes between entry and exit in 'HH:MM-HH:MM', or None if invalid."""
    if not isinstance(times, str):
        return None
    match = TIME_RANGE.fullmatch(times)
    if match is None:
        return None
    entry = _to_minutes(match.group(1), match.group(2))
    exit_time = _to_minutes(match.group(3), match.group(4))
    if entry is None or exit_time is None or exit_time < entry:
        return None
    return exit_time - entry


def hourly_rate(vehicle):
    """Hourly rate for bike/car/truck (any case, extra spaces OK), or None."""
    if not isinstance(vehicle, str):
        return None
    return RATES.get(vehicle.strip().lower())


def format_plate(plate):
    """Format 'ka01ab1234' as 'KA 01 AB 1234', or None if not a valid plate."""
    if not isinstance(plate, str) or not plate.isascii():
        return None
    p = plate.replace(" ", "").replace("-", "").upper()
    if not PLATE.fullmatch(p):
        return None
    return p[0:2] + " " + p[2:4] + " " + p[4:6] + " " + p[6:10]


def main():
    print("==== Running minutes_parked ====")
    user_input = input("Enter entry and exit time (e.g. 09:30-11:45): ")
    result = minutes_parked(user_input)
    if result is None:
        print("Invalid time range. Use HH:MM-HH:MM with exit after entry.")
    else:
        print("Minutes Parked:", result)

    print("\n==== Running hourly_rate ====")
    user_input = input("Enter vehicle type (bike/car/truck): ")
    result = hourly_rate(user_input)
    if result is None:
        print("Unknown vehicle type. Choose bike, car or truck.")
    else:
        print("Hourly Rate:", result)

    print("\n==== Running format_plate ====")
    user_input = input("Enter a number plate (e.g. ka01ab1234): ")
    result = format_plate(user_input)
    if result is None:
        print("Invalid number plate. Expected format like KA01AB1234.")
    else:
        print("Formatted Plate:", result)


if __name__ == "__main__":
    main()
