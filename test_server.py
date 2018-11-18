import json
import pytest
import requests
from server import *

# REQUEST_REQUIRED_KEYS = [["patient_id", "attending_email", "user_age"],
#                          ["patient_id", "heart_rate"],
#                          ["patient_id", "heart_rate_average_since"]]


# @pytest.mark.parametrize("HR, age, expected", [
#     (200, 2, True),
#     (120, 2, False),
#     (110, 6000, True),
#     (110, 5000, False),
# ])
# def test_is_tachycardic(HR, age, expected):
#     assert is_tachycardic(HR, age) == expected


@pytest.mark.parametrize("r, expected", [
    ({"patient_id": 1, "attending_email": "hi@duke.edu", "user_age": 30}, True),
    ({"attending_email": "hi@duke.edu", "user_age": 30}, False),
    ({"patient_id": 1, "attending_email": "hi@duke.edu"}, False)
])
def test_validate_new_patient_request(r, expected):
    try:
        validate_new_patient_request(json.dumps(r))
    except ValidationError:
        assert expected is False
    except TypeError:
        assert expected is False
    else:
        assert expected is True