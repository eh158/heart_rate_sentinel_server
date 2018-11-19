import datetime
import sendgrid
import os
from sendgrid.helpers.mail import *
from flask import Flask, jsonify, request

app = Flask(__name__)

patientlib = {}

REQUEST_REQUIRED_KEYS = [["patient_id", "attending_email", "user_age"],
                         ["patient_id", "heart_rate"],
                         ["patient_id", "heart_rate_average_since"]]

USER_EMAIL = "eh158@duke.edu"


def send_tachy_email(patient, attending_email, sender_email):
    if not isinstance(patient, str):
        raise TypeError("Str expected")
    for i in [attending_email, sender_email]:
        if not isinstance(i, str):
            raise TypeError("Str expected")
        if "@" not in i:
            raise ValidationError("Invalid email")
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(sender_email)
    to_email = Email(attending_email)
    subject = "Tachycardic"
    content = Content("text/plain", "Patient " + patient + " is tachycardic")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


def is_tachycardic(heart_rate, age):
    tachy = [159, 166, 182, 179, 186, 169, 151, 137, 133, 130, 119, 100]
    if not isinstance(age, int):
        if not isinstance(age, float):
            raise TypeError('Float or int expected')
    elif not isinstance(heart_rate, int):
        if not isinstance(heart_rate, float):
            raise TypeError('Float or int expected')
    new_age = age * 365
    if new_age <= 2:  # two days
        if heart_rate >= tachy[0]:
            return True
        else:
            return False
    elif new_age <= 6:  # six days
        if heart_rate >= tachy[1]:
            return True
        else:
            return False
    elif new_age <= 21:  # 3 weeks
        if heart_rate >= tachy[2]:
            return True
        else:
            return False
    elif new_age <= 62:  # 2 months
        if heart_rate >= tachy[3]:
            return True
        else:
            return False
    elif new_age <= 153:  # 5 months
        if heart_rate >= tachy[4]:
            return True
        else:
            return False
    elif new_age <= 324:  # 11 months
        if heart_rate >= tachy[5]:
            return True
        else:
            return False
    elif new_age <= 730:
        if heart_rate >= tachy[6]:
            return True
        else:
            return False
    elif new_age <= 1460:
        if heart_rate >= tachy[7]:
            return True
        else:
            return False
    elif new_age <= 2555:
        if heart_rate >= tachy[8]:
            return True
        else:
            return False
    elif new_age <= 4015:
        if heart_rate >= tachy[9]:
            return True
        else:
            return False
    elif new_age <= 5475:
        if heart_rate >= tachy[10]:
            return True
        else:
            return False
    else:
        if heart_rate >= tachy[11]:
            return True
        else:
            return False


class ValidationError(Exception):
    def __init__(self, message):
        self.message = message


def validate_new_patient_request(req):
    for key in REQUEST_REQUIRED_KEYS[0]:
        if key not in req.keys():
            raise ValidationError("Key '{0}' not found".format(key))


def validate_heart_rate_request(req):
    for key in REQUEST_REQUIRED_KEYS[1]:
        if key not in req.keys():
            raise ValidationError("Key '{0}' not found".format(key))


def validate_internal_average_request(req):
    for key in REQUEST_REQUIRED_KEYS[2]:
        if key not in req.keys():
            raise ValidationError("Key '{0}' not found".format(key))


@app.route("/api/new_patient/", methods=["POST"])
def new_patient():
    r = request.get_json()
    try:
        validate_new_patient_request(r)
    except ValidationError as inst:
        return jsonify({"message": inst.message}), 500
    if r['patient_id'] in patientlib.keys():
        return jsonify('Already initialized')
    else:
        patient = r['patient_id']
        patientlib[patient] = {}
        patientlib[patient]['attending_email'] = r['attending_email']
        patientlib[patient]['user_age'] = r['user_age']
        patientlib[patient]['heart_rate'] = []
        return jsonify('Initialized patient')


@app.route("/api/heart_rate/", methods=["POST"])
def heart_rate():
    r = request.get_json()
    try:
        validate_heart_rate_request(r)
    except ValidationError as inst:
        return jsonify({"message": inst.message}), 500
    if r['patient_id'] in patientlib.keys():
        patient = r['patient_id']
        hrdata = [r['heart_rate'], datetime.datetime.now()]
        patientlib[patient]['heart_rate'].append(hrdata)
        return jsonify('Added HR')
    else:
        return jsonify('Patient not Initialized')


@app.route("/api/status/<patient_id>", methods=["GET"])
def get_status(patient_id):
    HR_data = patientlib[patient_id]['heart_rate']
    HR_data_cut = [i[0] for i in HR_data]
    check = is_tachycardic(HR_data_cut, patientlib[patient_id]['user_age'])
    if (check):
        send_tachy_email(patient_id, patientlib[patient_id]['attending_email'], USER_EMAIL)


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def get_heart_rate(patient_id):
    HR_data = patientlib[patient_id]['heart_rate']
    HR_data_cut = [i[0] for i in HR_data]
    return jsonify(HR_data_cut)


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def get_heart_rate_avg(patient_id):
    HR_data = patientlib[patient_id]['heart_rate']
    HR_data_cut = [i[0] for i in HR_data]
    avg_HR = sum(HR_data_cut) / len(HR_data_cut)
    return jsonify(avg_HR)


@app.route("/api/heart_rate/internal_average/", methods=["POST"])
def internal_average():
    r = request.get_json()
    try:
        validate_internal_average_request(r)
    except ValidationError as inst:
        return jsonify({"message": inst.message}), 500
    patient = r['patient_id']
    target_time = r['heart_rate_average_since']
    HR_data = patientlib[patient]['heart_rate']
    HR_data_cut = [i[0] for i in HR_data if i[1] > target_time]
    avg_HR = sum(HR_data_cut) / len(HR_data_cut)
    return jsonify(avg_HR)


if __name__ == "__main__":
    app.run(host="127.0.0.1")
