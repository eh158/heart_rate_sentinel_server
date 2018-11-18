import pytest
import requests
from server import *


@pytest.mark.parametrize("patients, responses", [
    ([[0, "hi@duke.edu", 10]], ["added"]),
    ([[0, "hi@duke.edu", 10], [0, "hi@duke.edu", 10]],
     ["Initialized patient", "Already initialized"])
])
def test_new_patient(patients, responses):
    app.run(host="127.0.0.1")
    results = []
    for i in patients:
        r = requests.post("http://127.0.0.1:5000/api/new_patient/",
                          json={"patient_id": i[0],
                                "attending_email": i[1],
                                "user_age": i[2]})
        results.append(r.json())
    for j in range(len(results)):
        assert results[j] == responses[j]