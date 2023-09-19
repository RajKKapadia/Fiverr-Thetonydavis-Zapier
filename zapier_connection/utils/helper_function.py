import os
import re

import pandas as pd

from config import config


def clean_string_get_number(text: str) -> int:
    text = text.split('.')[0]
    text = re.sub('\D', '', text)
    text = int(text)
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
    age_req = clean_string_get_number(body['age_req'])
    service_hours = clean_string_get_number(body['service_req_hours'])
    service_duration = clean_string_get_number(body['service_req_period'])
    entry_option = body['entry_date']
    for i, row in csv_data.iterrows():
        this_age = int(row['Current_Age'])
        this_los = int(row['Length_of_Service'])
        this_hos = int(row['Hours_of_Service'])
        this_doh = row['Date_of_Hire']

        this_pytc = clean_string_get_number(row['Prior_Year_Compensation'])
        this_op = clean_string_get_number(row['Ownership_Percent'])
        this_fr = row['Family_Relationship']

        this_planytc = clean_string_get_number(
            row['Plan_Year_Total_Compensation'])
        this_pyed = clean_string_get_number(
            row['Plan_Year_Employee_Deferrals'])

        '''This is for eligibity
        (1) Checking for the entry option
        (2) Testing the eligibilty of the employee
        '''
        flag = False

        if entry_option == 'Immediate' and row['Current Date'] > this_doh:
            flag = True

        if entry_option == 'Semi-Annual':
            if (this_doh + pd.DateOffset(months=12)) <= (csv_data.at[i, 'Current Date'] - pd.DateOffset(months=6)):
                flag = True

        if entry_option == 'Quarterly':
            if (this_doh + pd.DateOffset(months=12)) <= (csv_data.at[i, 'Current Date'] - pd.DateOffset(months=3)):
                flag = True

        if entry_option == 'Monthly':
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
        'response_data': []
    }

    for i, row in csv_data.iterrows():
        reponse_data['response_data'].append(row.to_dict())

    return reponse_data


def convert_data_to_csv(data: dict) -> str:
    csv_data = pd.DataFrame.from_dict(data)
    csv_data.to_csv(config.CSV_FILE_PATH, index=False)
    return config.CSV_FILE_PATH
