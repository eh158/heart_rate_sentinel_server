import datetime
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
        patientlib[patient] = {}
        patientlib[patient]['attending_email'] = r['attending_email']
        patientlib[patient]['user_age'] = r['user_age']
        patientlib[patient]['heart_rate'] =[]
        return jsonify('Initialized patient')


@app.route("/api/heart_rate/", methods=["POST"])
def heart_rate():
    r = request.get_json()
    if r['patient_id'] in patientlib.keys():
        patient = r['patient_id']
        hrdata = [r['heart_rate'], datetime.datetime.now()]
        patientlib[patient]['heart_rate'].append(hrdata)
        return jsonify('Added HR')
    else:
        return jsonify('Patient not Initialized')


if __name__ == "__main__":
    app.run(host="127.0.0.1")
