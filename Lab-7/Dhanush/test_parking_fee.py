"""Lab 7 - Fuzz tests for parking_fee.py using Hypothesis.

Name: Dhanush S S | SRN: PES1UG24AM082 | Section: B

Run:
    python -m pytest test_parking_fee.py

Two kinds of tests for each function:
  1. "no crash" fuzz tests - random text / None must never raise.
  2. property tests - valid input gives the right answer, and the
     output always has the expected shape (or is None for bad input).
"""
import re

from hypothesis import given, settings, strategies as st

from parking_fee import minutes_parked, hourly_rate, format_plate

# Anything at all: random unicode text, None, numbers, lists.
any_input = st.text() | st.none() | st.integers() | st.floats() | st.lists(st.text())

# Inputs shaped like the real thing, so the fuzzer gets past the first
# split and reaches the deeper bugs.
time_like = st.from_regex(r"\A\s*-?\d{0,3}:\d{0,3}\s*-\s*-?\d{0,3}:\d{0,3}\s*\Z")
plate_like = st.from_regex(r"\A[A-Za-z0-9 -]{0,14}\Z")

hours = st.integers(min_value=0, max_value=23)
mins = st.integers(min_value=0, max_value=59)

PLATE_OUT = re.compile(r"[A-Z]{2} [0-9]{2} [A-Z]{2} [0-9]{4}")


# ======================= minutes_parked =======================

@given(st.text() | st.none())
def test_minutes_parked_no_crash(s):
    try:
        minutes_parked(s)
    except Exception as e:
        assert False, f"minutes_parked crashed with: {e!r}"


@given(any_input | time_like)
def test_minutes_parked_no_crash_on_shaped_input(s):
    try:
        minutes_parked(s)
    except Exception as e:
        assert False, f"minutes_parked crashed with: {e!r}"


@given(any_input | time_like)
def test_minutes_parked_never_negative_or_too_long(s):
    result = minutes_parked(s)
    assert result is None or (isinstance(result, int) and 0 <= result <= 24 * 60), \
        f"minutes_parked({s!r}) returned {result!r}"


@given(hours, mins, hours, mins)
def test_minutes_parked_valid_times(h1, m1, h2, m2):
    start, end = h1 * 60 + m1, h2 * 60 + m2
    s = f"{h1:02d}:{m1:02d}-{h2:02d}:{m2:02d}"
    if end >= start:
        assert minutes_parked(s) == end - start
    else:
        # exit before entry is not a valid stay
        assert minutes_parked(s) is None


# ======================= hourly_rate =======================

@given(st.text() | st.none())
def test_hourly_rate_no_crash(s):
    try:
        hourly_rate(s)
    except Exception as e:
        assert False, f"hourly_rate crashed with: {e!r}"


@given(any_input)
def test_hourly_rate_returns_known_rate_or_none(s):
    assert hourly_rate(s) in (None, 10, 30, 60)


@given(
    st.sampled_from([("bike", 10), ("car", 30), ("truck", 60)]),
    st.text(alphabet=" \t", max_size=3),
    st.text(alphabet=" \t", max_size=3),
    st.booleans(),
)
def test_hourly_rate_valid_vehicles(pair, left, right, upper):
    name, rate = pair
    name = name.upper() if upper else name
    assert hourly_rate(left + name + right) == rate


# ======================= format_plate =======================

@given(st.text() | st.none())
def test_format_plate_no_crash(s):
    try:
        format_plate(s)
    except Exception as e:
        assert False, f"format_plate crashed with: {e!r}"


@given(any_input | plate_like)
def test_format_plate_output_is_well_formed(s):
    result = format_plate(s)
    assert result is None or PLATE_OUT.fullmatch(result), \
        f"format_plate({s!r}) returned {result!r}"


@settings(max_examples=200)
@given(st.from_regex(r"\A[A-Za-z]{2}[0-9]{2}[A-Za-z]{2}[0-9]{4}\Z"))
def test_format_plate_valid_plates(p):
    up = p.upper()
    assert format_plate(p) == f"{up[0:2]} {up[2:4]} {up[4:6]} {up[6:10]}"
