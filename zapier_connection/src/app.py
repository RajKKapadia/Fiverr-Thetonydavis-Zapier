from flask import Flask, request, jsonify

from zapier_connection.utils.helper_function import text_to_csv, process_csv_data, check_conditions

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def handle_home():
    return 'OK', 200


@app.route('/webhook', methods=['POST'])
def handle_webhook():
    body = request.get_json()
    print(body)
    csv_data = text_to_csv(body['Census_Data'])
    processed_data = process_csv_data(csv_data, body)
    final_data = check_conditions(processed_data, body)
    return jsonify(
        {
            'response_data': final_data
        }
    )
