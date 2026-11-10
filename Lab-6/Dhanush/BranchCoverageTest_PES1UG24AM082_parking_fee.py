"""Lab 6 - Branch coverage tests for parking_fee.py.

Name: Dhanush S S | SRN: PES1UG24AM082 | Section: B

Goal: make every decision in parking_fee.py take both its True and its
False path at least once.
Run:
    coverage run --branch -m pytest BranchCoverageTest_PES1UG24AM082_parking_fee.py
    coverage report -m

Decision table (T = True path, F = False path):
  parking_fee
    vehicle not in HOURLY_RATE   T: bus            F: car/bike/truck
    minutes < 0                  T: -5             F: 0 and up
    minutes <= 30                T: 0, 20, 30      F: 31, 60, 90 ...
    minutes % 60 != 0            T: 31, 90         F: 60, 120 (exact hours)
    is_ev and vehicle != truck   T: EV car/bike    F: EV truck, non-EV
    lost_ticket                  T / F
  find_slot
    free_slots <= 0              T: 0, -1          F: 1+
    is_disabled                  T / F
    vehicle == "truck"           T / F
  monthly_pass
    vehicle == "bike"            T / F
    vehicle == "car"             T / F (truck -> ValueError)
    is_resident                  T / F
"""
import pytest
from parking_fee import parking_fee, find_slot, monthly_pass


# ======================= parking_fee =======================

# -- input validation --
@pytest.mark.parametrize("vehicle", ["bus", "", "Car", "scooter"])
def test_unknown_vehicle_raises(vehicle):
    with pytest.raises(ValueError, match="unknown vehicle"):
        parking_fee(vehicle, 60, False, False)


def test_negative_minutes_raises():
    with pytest.raises(ValueError, match="invalid duration"):
        parking_fee("car", -1, False, False)


# -- free period: minutes <= 30 (True) --
@pytest.mark.parametrize("minutes", [0, 20, 30])
def test_free_period(minutes):
    assert parking_fee("car", minutes, False, False) == 0


# -- paid period, partial hour: minutes % 60 != 0 (True) --
@pytest.mark.parametrize(
    "vehicle, minutes, expected",
    [
        ("car", 31, 30),      # just over free limit -> 1 hour
        ("car", 90, 60),      # 1h30 -> 2 hours
        ("bike", 61, 20),     # 1h01 -> 2 hours
        ("truck", 150, 180),  # 2h30 -> 3 hours
    ],
)
def test_partial_hour_rounds_up(vehicle, minutes, expected):
    assert parking_fee(vehicle, minutes, False, False) == expected


# -- paid period, exact hours: minutes % 60 != 0 (False) --
@pytest.mark.parametrize(
    "vehicle, minutes, expected",
    [
        ("car", 60, 30),
        ("bike", 120, 20),
        ("truck", 180, 180),
    ],
)
def test_exact_hours_not_rounded(vehicle, minutes, expected):
    assert parking_fee(vehicle, minutes, False, False) == expected


# -- EV discount: is_ev and vehicle != "truck" --
def test_ev_car_half_price():
    assert parking_fee("car", 120, True, False) == 30


def test_ev_bike_half_price_rounds_down():
    # 1 hour bike = 10 -> 10 // 2 = 5
    assert parking_fee("bike", 60, True, False) == 5


def test_ev_truck_gets_no_discount():
    # is_ev is True but vehicle is truck -> condition False
    assert parking_fee("truck", 60, True, False) == 60


def test_ev_in_free_period_stays_free():
    assert parking_fee("car", 15, True, False) == 0


# -- lost ticket --
def test_lost_ticket_adds_penalty():
    assert parking_fee("car", 60, False, True) == 230


def test_lost_ticket_in_free_period():
    assert parking_fee("bike", 10, False, True) == 200


def test_ev_and_lost_ticket_combined():
    # penalty is added AFTER the EV discount: 60 // 2 + 200
    assert parking_fee("car", 120, True, True) == 230


# ======================= find_slot =======================

@pytest.mark.parametrize("free_slots", [0, -1])
def test_full_when_no_slots(free_slots):
    assert find_slot("car", free_slots, False) == "full"


def test_full_beats_disabled():
    # full check comes first, even for a disabled driver
    assert find_slot("car", 0, True) == "full"


def test_disabled_gets_ground_floor():
    assert find_slot("bike", 1, True) == "ground floor"


def test_disabled_truck_gets_ground_floor():
    # disabled check comes before the truck check
    assert find_slot("truck", 4, True) == "ground floor"


def test_truck_goes_to_basement():
    assert find_slot("truck", 2, False) == "basement"


@pytest.mark.parametrize("vehicle", ["car", "bike"])
def test_other_vehicles_any_floor(vehicle):
    assert find_slot(vehicle, 5, False) == "any floor"


# ======================= monthly_pass =======================

@pytest.mark.parametrize(
    "vehicle, is_resident, expected",
    [
        ("bike", False, 500),
        ("bike", True, 400),    # 500 - 500 // 5
        ("car", False, 1500),
        ("car", True, 1200),    # 1500 - 1500 // 5
    ],
)
def test_monthly_pass_prices(vehicle, is_resident, expected):
    assert monthly_pass(vehicle, is_resident) == expected


@pytest.mark.parametrize("vehicle", ["truck", "bus"])
def test_no_pass_for_other_vehicles(vehicle):
    with pytest.raises(ValueError, match="no pass for this vehicle"):
        monthly_pass(vehicle, True)
