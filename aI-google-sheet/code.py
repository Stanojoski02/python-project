import requests
# from __future__ import print_function
import datetime

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'

cerd = None
cerd = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID spreadsheet.

SAMPLE_SPREADSHEET_ID = '18B7uJiOdnUGOQsUIMUAAXuiBt2sEWyC04OUQJZTEb-s'


service = build('sheets', 'v4', credentials=cerd)

    # Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range="workouts!A1:E24").execute()




with open("num.txt","r") as data:
    a = int(data.read())
while True:
    bojan = input("Do you have anything to enter today? y/n: ")
    if bojan=="y":
        nutrition_api_key = "c59ab0125ab2b1be9d188a2681a0f51e"
        nutrition_api_id = "1577eb4b"
        nutrition_url = "https://trackapi.nutritionix.com/v2/natural/exercise"
        exercise_text = input("Tell me wich exercises you did: ")
        headers = {
            "x-app-id": nutrition_api_id,
            "x-app-key": nutrition_api_key
        }
        parameters = {
            "query": exercise_text,
            "gender": "male",
            "weight_kg": 73,
            "height_cm": 182,
            "age": 19
        }
        response = requests.post(url=nutrition_url, json=parameters, headers=headers)
        resultt = response.json()
        print(resultt)
        calories = resultt["exercises"][0]["nf_calories"]
        exercise = resultt["exercises"][0]["name"].title()
        duration = resultt["exercises"][0]["duration_min"]
        date = f"{datetime.datetime.now().day}/{datetime.datetime.now().month}/{datetime.datetime.now().year}"
        time = f"{datetime.datetime.now().time().hour}:{datetime.datetime.now().time().minute}"


        values = result.get('values', [])

        aaa = [[date,time,exercise,f"{duration}min",calories]]
        request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                            range=f"workouts!A{a}", valueInputOption="USER_ENTERED", body={"values":aaa}).execute()
        print("Your daily activities are saved")
        a+=1
        with open("num.txt", "w") as data:
            data.write(str(a))
    else:
        break
