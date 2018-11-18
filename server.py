import request
from flask import Flask, jsonify, request
app = Flask(__name__)

patientlib = {}

@app.route("/api/new_patient/", methods=["POST"])
def new_patient():
    r = request.get_json()
    if r['patient_id'] in patientlib.keys():
        return jsonify('Already initialized')
    else:
        patient = r['patient_id']
        patientlib[patient]={}
        patientlib[patient]['attending_email']=r['attending_email']
        patientlib[patient]['user_age']=r['user_age']
        return jsonify('Initialized patient')


if __name__ == "__main__":
    app.run(host="127.0.0.1")