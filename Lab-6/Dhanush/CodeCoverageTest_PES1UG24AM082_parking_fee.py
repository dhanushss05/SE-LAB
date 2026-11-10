"""Lab 6 - Code (line) coverage tests for parking_fee.py.

Name: Dhanush S S | SRN: PES1UG24AM082 | Section: B

Goal: execute every line of parking_fee.py at least once.
Run:
    coverage run -m pytest CodeCoverageTest_PES1UG24AM082_parking_fee.py
    coverage report -m
"""
import pytest
from parking_fee import parking_fee, find_slot, monthly_pass


# ---------- starter tests from the repo ----------
def test_free_short_stay():
    assert parking_fee("car", 20, False, False) == 0


def test_any_floor():
    assert find_slot("car", 5, False) == "any floor"


# ---------- parking_fee ----------
def test_unknown_vehicle_raises():
    with pytest.raises(ValueError, match="unknown vehicle"):
        parking_fee("bus", 60, False, False)


def test_negative_minutes_raises():
    with pytest.raises(ValueError, match="invalid duration"):
        parking_fee("car", -5, False, False)


def test_partial_hour_rounds_up():
    # 90 minutes -> 1 full hour + leftover 30 min -> billed as 2 hours
    assert parking_fee("car", 90, False, False) == 60


def test_ev_car_gets_half_price():
    # 90 min car = 60, EV discount halves it
    assert parking_fee("car", 90, True, False) == 30


def test_lost_ticket_adds_penalty():
    assert parking_fee("bike", 20, False, True) == 200


# ---------- find_slot ----------
def test_no_free_slots_is_full():
    assert find_slot("car", 0, False) == "full"


def test_disabled_gets_ground_floor():
    assert find_slot("car", 3, True) == "ground floor"


def test_truck_goes_to_basement():
    assert find_slot("truck", 3, False) == "basement"


# ---------- monthly_pass ----------
def test_bike_pass():
    assert monthly_pass("bike", False) == 500


def test_car_pass_resident_discount():
    # 1500 - 1500 // 5 = 1200
    assert monthly_pass("car", True) == 1200


def test_truck_has_no_pass():
    with pytest.raises(ValueError, match="no pass for this vehicle"):
        monthly_pass("truck", False)
