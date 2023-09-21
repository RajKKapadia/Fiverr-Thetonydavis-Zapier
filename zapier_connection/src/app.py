import json

from flask import Flask, request, jsonify, send_file

from zapier_connection.utils.helper_function import text_to_csv, process_csv_data, check_conditions, convert_data_to_csv

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def handle_home():
    return 'OK', 200


@app.route('/processData', methods=['POST'])
def handle_process_data():
    body = request.get_json()
    print(body)
    csv_data = text_to_csv(body['Census_Data'])
    processed_data = process_csv_data(csv_data, body)
    response_data = check_conditions(processed_data, body)
    print(response_data)
    return jsonify(json.dumps(response_data))


@app.route('/eligibility_status_report', methods=['POST'])
def handle_eligibility_status_report():
    body = request.get_json()
    print(body)
    response_data = json.loads(body['eligibility_status_report'])
    csv_file_path = convert_data_to_csv(response_data['eligibility_status_report'])
    return send_file(csv_file_path, mimetype='text/csv')

@app.route('/hce_nhce_status_report', methods=['POST'])
def handle_hce_nhce_status_report():
    body = request.get_json()
    print(body)
    response_data = json.loads(body['hce_nhce_status_report'])
    csv_file_path = convert_data_to_csv(response_data['hce_nhce_status_report'])
    return send_file(csv_file_path, mimetype='text/csv')

@app.route('/eligible_hce_report', methods=['POST'])
def handle_eligible_hce_report():
    body = request.get_json()
    print(body)
    response_data = json.loads(body['eligible_hce_report'])
    csv_file_path = convert_data_to_csv(response_data['eligible_hce_report'])
    return send_file(csv_file_path, mimetype='text/csv')

@app.route('/eligible_nhce_report', methods=['POST'])
def handle_eligible_nhce_report():
    body = request.get_json()
    print(body)
    response_data = json.loads(body['eligible_nhce_report'])
    csv_file_path = convert_data_to_csv(response_data['eligible_nhce_report'])
    return send_file(csv_file_path, mimetype='text/csv')
