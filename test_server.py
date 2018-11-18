import json
import pytest
import requests
from server import *


# REQUEST_REQUIRED_KEYS = [["patient_id", "attending_email", "user_age"],
#                          ["patient_id", "heart_rate"],
#                          ["patient_id", "heart_rate_average_since"]]


@pytest.mark.parametrize("HR, age, expected, broke", [
    (200, 2, True, False),
    (120, 2, False, False),
    (110, 6000, True, False),
    (101, 5000, False, False),
    ("abc", 5000, False, True),
    (100, "abc", False, True),
])
def test_is_tachycardic(HR, age, expected, broke):
    age_years = float(age)/float(365)
    try:
        out = is_tachycardic(HR, age_years)
    except TypeError:
        assert broke is True
    else:
        assert broke is False
        assert out == expected


@pytest.mark.parametrize("r, broke", [
    ({"patient_id": "1", "attending_email": "hi@duke.edu", "user_age": 30},
     False),
    ({"attending_email": "hi@duke.edu", "user_age": 30}, True),
    ({"patient_id": "1", "attending_email": "hi@duke.edu"}, True)
])
def test_validate_new_patient_request(r, broke):
    try:
        validate_new_patient_request(r)
    except ValidationError:
        assert broke is True
    except TypeError:
        assert broke is True
    else:
        assert broke is False


@pytest.mark.parametrize("r, broke", [
    ({"patient_id": "1", "heart_rate": 30}, False),
    ({"patient_id": "1"}, True),
    ({"heart_rate": 30}, True),
    ({"patient_id": "1", "heart_rate": 30,
      "attending_email": "hi@duke.edu"}, False),
])
def test_validate_heart_rate_request(r, broke):
    try:
        validate_heart_rate_request(r)
    except ValidationError:
        assert broke is True
    except TypeError:
        assert broke is True
    else:
        assert broke is False


@pytest.mark.parametrize("r, broke", [
    ({"patient_id": "1",
      "heart_rate_average_since": "2018-03-09 11:00:36.372339"}, False),
    ({"patient_id": "1"}, True),
    ({"heart_rate_average_since": "2018-03-09 11:00:36.372339"}, True),
    ({"patient_id": "1",
      "heart_rate_average_since": "2018-03-09 11:00:36.3", "hi": 0}, False)
])
def test_validate_internal_average_request(r, broke):
    try:
        validate_internal_average_request(r)
    except ValidationError:
        assert broke is True
    except TypeError:
        assert broke is True
    else:
        assert broke is False
