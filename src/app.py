from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def handle_home():
    return 'OK', 200


@app.route('/webhook', methods=['POST'])
def handle_webhook():
    body = request.get_json()
    print(body)
    '''Process the information
    '''
    # import csv
    # import requests
    # from dateutil.relativedelta import relativedelta
    # from datetime import datetime
    # from io import StringIO
    # import json

    # # Get HCE_threshold from input_data or default, remove symbols, and convert to integer
    # HCE_threshold_str = input_data.get('HCE_threshold')
    # HCE_threshold = int(HCE_threshold_str.replace('$', '').replace(',', ''))

    # # Initialize lists and counters
    # HCE_details = []
    # NHCE_details = []
    # ineligible_details = []
    # total_deferral_HCE = 0
    # total_deferral_NHCE = 0
    # count_HCE = 0
    # count_NHCE = 0

    # # Assuming input_data is provided with necessary keys
    # csv_data = None

    # # Length of Service mapping, can be passed as a JSON string and parsed
    # length_of_service_map = json.loads(input_data.get('length_of_service_map'))

    # # Assuming CSV data is provided via URL
    # if 'csv_url' in input_data:
    #     response = requests.get(input_data['csv_url'])
    #     csv_data = StringIO(response.text)

    # # Alternatively, assuming CSV data is provided as content
    # elif 'csv_content' in input_data:
    #     csv_data = StringIO(input_data['csv_content'])

    # # Initialize the CSV reader
    # reader = csv.DictReader(csv_data)

    # # Initializations
    # summary_output = ""
    # HCE_details = []
    # NHCE_details = []
    # ineligible_details = []  # List to keep track of ineligible participants
    # total_deferral_HCE = 0
    # total_deferral_NHCE = 0
    # count_HCE = 0
    # count_NHCE = 0
    # HCE_threshold = 135000

    # # Allowable compensation limit from input data
    # allowable_compensation_limit = float(
    #     input_data.get('allowable_compensation_limit'))

    # # Process the CSV data
    # for row in reader:
    #     name = row['NAME (LAST, FIRST)']
    #     hire_date = datetime.strptime(
    #         row['Original Date of Hire  (mm/dd/yyyy)'], '%m/%d/%Y')
    #     compensation = float(row['Total Compensation'].replace(',', ''))
    #     deferral = float(row['401(k)/403(b) Employee Deferrals'].replace(',', ''))
    #     hours_of_service = int(row['Hours of Service'])
    #     allowable_compensation = min(compensation, 305000)  # Limit to 305K
    #     deferral_percentage = (deferral / allowable_compensation) * 100
    #     excess_contribution = max(
    #         0, deferral - allowable_compensation * (deferral_percentage / 100))

    #     if compensation >= HCE_threshold:
    #         detail = {
    #             'Name': name,
    #             'Total Compensation': int(compensation),
    #             'Allowable Compensation': int(allowable_compensation),
    #             'Deferral %': round(deferral_percentage, 2),
    #             'Total Deferred Amount': int(deferral),
    #             'Excess Contribution': int(excess_contribution)
    #         }
    #         HCE_details.append(detail)
    #         total_deferral_HCE += deferral_percentage
    #         count_HCE += 1
    #     else:
    #         # Assuming 'length_of_service_map' contains eligibility criteria and 'hire_date' is available
    #         length_of_service = relativedelta(datetime.now(), hire_date).years
    #         # Replace 0 with the default eligibility criteria
    #         if length_of_service >= length_of_service_map.get("NHCE", 0):
    #             NHCE_details.append(
    #                 f"{name} defers {deferral_percentage:.2f}% with Excess Contribution: ${int(excess_contribution):,}")
    #             total_deferral_NHCE += deferral_percentage
    #             count_NHCE += 1
    #         else:
    #             ineligible_details.append(
    #                 f"{name} is ineligible due to less length of service.")

    # # Calculate the average deferral percentages
    # average_deferral_percentage_HCE = total_deferral_HCE / \
    #     count_HCE if count_HCE > 0 else 0
    # average_deferral_percentage_NHCE = total_deferral_NHCE / \
    #     count_NHCE if count_NHCE > 0 else 0

    # # Calculate the difference between HCE and NHCE average deferral percentages
    # difference_between_HCE_and_NHCE = average_deferral_percentage_HCE - \
    #     average_deferral_percentage_NHCE

    # # Apply the ADP test rules
    # if (average_deferral_percentage_HCE - average_deferral_percentage_NHCE <= 2) or \
    #    (average_deferral_percentage_HCE / average_deferral_percentage_NHCE <= 2):
    #     adp_test_result = "Pass"
    # else:
    #     adp_test_result = "Fail"

    # # Create a dictionary to store the summary information
    # summary_dict = {
    #     'HCE_details': HCE_details,
    #     'NHCE_details': NHCE_details,
    #     'ineligible_details': ineligible_details,
    #     'average_deferral_percentage_HCE': average_deferral_percentage_HCE,
    #     'average_deferral_percentage_NHCE': average_deferral_percentage_NHCE,
    #     'difference_between_HCE_and_NHCE': difference_between_HCE_and_NHCE,
    #     'adp_test_result': adp_test_result
    # }

    # # Return the summary dictionary (make sure to return this in your Zapier step)
    # return jsonify(summary_dict)
    return jsonify(
        {
            'key': 'value',
            'key1': 'value1',
            'key2': 'value2'
        }
    )
