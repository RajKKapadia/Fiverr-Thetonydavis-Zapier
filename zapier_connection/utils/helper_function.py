import os
import re

import pandas as pd

from config import config


def remove_commas_get_int(text) -> int:  # Removed the str type hint
    print(f"Type: {type(text)}, Value: {text}")
    if isinstance(text, str):
        text = re.sub('\D', '', text)
    text = int(text)
    return text



def remove_percentage_get_float(text: str) -> float:
    text = text.replace('%', '')
    text = float(text)
    return text


def text_to_csv(text: str) -> pd.DataFrame:
    with open(config.TEXT_FILE_PATH, 'w') as file:
        file.write(text)
    csv_data = pd.read_csv(config.TEXT_FILE_PATH)
    os.unlink(config.TEXT_FILE_PATH)
    return csv_data


def process_csv_data(csv_data: pd.DataFrame, body: dict) -> pd.DataFrame:
    csv_data['Date_of_Birth'] = csv_data['Date_of_Birth'].apply(pd.to_datetime)
    csv_data['Date_of_Hire'] = csv_data['Date_of_Hire'].apply(pd.to_datetime)
    csv_data['Current Date'] = body['end_of_plan_year']
    csv_data['Current Date'] = csv_data['Current Date'].apply(pd.to_datetime)
    csv_data['Current_Age'] = (
        csv_data['Current Date'].dt.year - csv_data['Date_of_Birth'].dt.year).astype(int)
    csv_data['Length_of_Service'] = (
        csv_data['Current Date'].dt.year - csv_data['Date_of_Hire'].dt.year).astype(int) * 12
    csv_data['Eligible_Status'] = 'Not_Eligible'
    csv_data['HCE_NHCE'] = 'NHCE'
    csv_data['Plan_Year_Deferral_Percent'] = '0.0%'
    return csv_data


def check_conditions(csv_data: pd.DataFrame, body: dict) -> dict:
    age_req = remove_commas_get_int(body['age_req'])
    service_hours = remove_commas_get_int(body['service_req_hours'])
    service_duration = remove_commas_get_int(body['service_req_period'])
    entry_option = body['entry_date']
    
    for i, row in csv_data.iterrows():
        this_age = int(row['Current_Age'])
        this_los = int(row['Length_of_Service'])
        this_hos = int(row['Hours_of_Service'])
        this_doh = row['Date_of_Hire']

        flag = False

        if entry_option == 'Immediate' and row['Current Date'] > this_doh:
            flag = True
        elif entry_option == 'Semi-Annual':
            if this_doh <= (csv_data.at[i, 'Current Date'] - pd.DateOffset(months=3)):
                flag = True
        elif entry_option == 'Quarterly':
            if (this_doh + pd.DateOffset(months=12)) <= (csv_data.at[i, 'Current Date'] - pd.DateOffset(months=3)):
                flag = True
        elif entry_option == 'Monthly':
            if (this_doh + pd.DateOffset(months=12)) <= (csv_data.at[i, 'Current Date'] - pd.DateOffset(months=1)):
                flag = True

        if flag and this_age > age_req and this_los >= service_duration and this_hos >= service_hours:
            csv_data.at[i, 'Eligible_Status'] = 'Eligible'

        '''This is for HCE
        (1) Checking highly compensated employee
        '''
        if this_pytc >= config.HCE_AMOUNT or this_op >= config.HCE_OWNERSHIP_PERCENTAGE or this_fr == config.HCE_FAMILY_RELATIONSHIP:
            csv_data.at[i, 'HCE_NHCE'] = 'HCE'

        '''This is for deferral percentage
        (1) Checking the plan year total compensation is less than config.DP_MAXIMUM_COMPENSATION
        (2) Calculating Deferral_Percentage
        '''
        if this_planytc >= config.DP_MAXIMUM_COMPENSATION:
            this_planytc = config.DP_MAXIMUM_COMPENSATION
        csv_data.at[i,
                    'Plan_Year_Deferral_Percent'] = f'{round(((this_pyed / this_planytc) * 100), 2)}%'

    for col in csv_data.columns:
        if csv_data[col].dtype == 'datetime64[ns]':
            csv_data[col] = csv_data[col].dt.strftime('%Y/%m/%d')

    reponse_data = {
        'eligibility_status_report': generate_eligibility_status_report(csv_data),
        'hce_nhce_status_report': generate_hce_nhce_status_report(csv_data),
        'eligible_hce_report': generate_eligible_hce_report(csv_data),
        'eligible_nhce_report': generate_eligible_nhce_report(csv_data),
        'final_report': generate_final_report(csv_data)
    }

    return reponse_data


def generate_eligibility_status_report(csv_data: pd.DataFrame) -> list[dict]:
    eligibility_status_report = []
    needed_columns = ['First_Name', 'Last_Name', 'Current_Age',
                      'Plan_Year_Total_Compensation', 'Plan_Year_Deferral_Percent', 'Hours_of_Service', 'Eligible_Status']
    new_csv_data = csv_data[needed_columns]
    new_csv_data.sort_values(
        by=['Eligible_Status'], ascending=False).reset_index(drop=True)
    for _, row in new_csv_data.iterrows():
        eligibility_status_report.append(row.to_dict())
    return eligibility_status_report


def generate_hce_nhce_status_report(csv_data: pd.DataFrame) -> list[dict]:
    hce_nhce_status_report = []
    needed_columns = ['First_Name', 'Last_Name', 'Current_Age', 'Plan_Year_Total_Compensation', 'Plan_Year_Deferral_Percent',
                      'Officer', 'Ownership_Percent', 'Family_Relationship', 'HCE_NHCE']
    new_csv_data = csv_data[needed_columns]
    new_csv_data.sort_values(
        by=['HCE_NHCE'], ascending=False).reset_index(drop=True)
    for _, row in new_csv_data.iterrows():
        hce_nhce_status_report.append(row.to_dict())
    return hce_nhce_status_report


def generate_eligible_hce_report(csv_data: pd.DataFrame) -> list[dict]:
    eligible_hce_report = []
    needed_columns = ['First_Name', 'Last_Name', 'Current_Age', 'Plan_Year_Total_Compensation', 'Plan_Year_Deferral_Percent',
                      'Officer', 'Ownership_Percent', 'Family_Relationship', 'HCE_NHCE']
    for _, row in csv_data.iterrows():
        if row['HCE_NHCE'] == 'HCE' and row['Eligible_Status'] == 'Eligible':
            new_row = row[needed_columns]
            eligible_hce_report.append(new_row.to_dict())
    return eligible_hce_report


def generate_eligible_nhce_report(csv_data: pd.DataFrame) -> list[dict]:
    eligible_nhce_report = []
    needed_columns = ['First_Name', 'Last_Name', 'Current_Age', 'Plan_Year_Total_Compensation', 'Plan_Year_Deferral_Percent',
                      'Officer', 'Ownership_Percent', 'Family_Relationship', 'HCE_NHCE']
    for _, row in csv_data.iterrows():
        if row['HCE_NHCE'] == 'NHCE' and row['Eligible_Status'] == 'Eligible':
            new_row = row[needed_columns]
            eligible_nhce_report.append(new_row.to_dict())
    return eligible_nhce_report


def generate_final_report(csv_data: pd.DataFrame) -> list[dict]:
    final_report = []
    needed_columns = ['First_Name', 'Last_Name', 'Date_of_Birth', 'Date_of_Hire', 'Current_Age', 'Eligible_Status', 'Prior_Year_Compensation',
                      'Plan_Year_Total_Compensation', 'Officer', 'Ownership_Percent', 'Family_Relationship', 'HCE_NHCE', 'Plan_Year_Deferral_Percent']
    new_csv_data = csv_data[needed_columns]
    for _, row in new_csv_data.iterrows():
        final_report.append(row.to_dict())
    return final_report


def convert_data_to_csv(data: dict) -> str:
    csv_data = pd.DataFrame.from_dict(data)
    csv_data.to_csv(config.CSV_FILE_PATH, index=False)
    return config.CSV_FILE_PATH


def handle_ccd(body: dict) -> dict:
    allowd_hce_limit = remove_percentage_get_float(body['Allowed_HCE_Limit'])
    average_hce = remove_percentage_get_float(body['Avg_HCE'])
    # average_nhce = body['Avg_NHCE']
    # hce_status = text_to_csv(body['HCE_Status'])
    max_allowed_compensation = int(body['Max_Allowed_Comp'])
    employee_data_csv = text_to_csv(body['employee_data_csv'])
    '''TODO
    [ ] Clean the columns
    '''
    employee_data_csv['Plan_Year_Total_Compensation'] = employee_data_csv['Plan_Year_Total_Compensation'].apply(
        remove_commas_get_int)

    excess_deferral_percentage = average_hce - allowd_hce_limit
    employee_data_csv['Excess_Percentage'] = round(
        excess_deferral_percentage, 2)
    employee_data_csv['Excess_Contribution'] = 0.0
    needed_columns = ['First_Name', 'Last_Name', 'HCE_NHCE',
                      'Plan_Year_Total_Compensation', 'Excess_Percentage', 'Excess_Contribution']
    correlative_destribution = []
    for i, row in employee_data_csv.iterrows():
        if row['HCE_NHCE'] == 'HCE':
            if row['Plan_Year_Total_Compensation'] >= max_allowed_compensation:
                row['Plan_Year_Total_Compensation'] = max_allowed_compensation
            row['Excess_Contribution'] = int((row['Plan_Year_Total_Compensation'] * row['Excess_Percentage']) / 100)
        row['Plan_Year_Total_Compensation'] = '{:,}'.format(row['Plan_Year_Total_Compensation'])
        row['Excess_Contribution'] = '{:,}'.format(row['Excess_Contribution'])
        new_row = row[needed_columns]
        correlative_destribution.append(new_row.to_dict())
    return correlative_destribution


def handle_qnce(body: dict) -> dict:
    allowd_hce_limit = remove_percentage_get_float(body['Allowed_HCE_Limit'])
    average_hce = remove_percentage_get_float(body['Avg_HCE'])
    employee_data_csv = text_to_csv(body['employee_data_csv'])
    '''TODO
    [ ] Clean the columns
    '''
    employee_data_csv['Plan_Year_Total_Compensation'] = employee_data_csv['Plan_Year_Total_Compensation'].apply(
        remove_commas_get_int)
    
    employee_data_csv['Individual_QNHCE'] = 0
    excess_deferral_percentage = average_hce - allowd_hce_limit
    total_compensation = employee_data_csv['Plan_Year_Total_Compensation'].sum()
    total_qnce = (excess_deferral_percentage * total_compensation) / 100
    needed_columns = ['First_Name', 'Last_Name', 'HCE_NHCE',
                      'Plan_Year_Total_Compensation', 'Individual_QNHCE']
    individual_qnhce = []
    for i, row in employee_data_csv.iterrows():
        row['Individual_QNHCE'] = int((row['Plan_Year_Total_Compensation'] / total_compensation) * total_qnce)
        row['Individual_QNHCE'] = '{:,}'.format(row['Individual_QNHCE'])
        row['Plan_Year_Total_Compensation'] = '{:,}'.format(row['Plan_Year_Total_Compensation'])
        new_row = row[needed_columns]
        individual_qnhce.append(new_row.to_dict())
    return individual_qnhce
