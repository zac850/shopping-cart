# for how to connect google & python:
# https://developers.google.com/sheets/api/quickstart/python 
# https://towardsdatascience.com/how-to-import-google-sheets-data-into-a-pandas-dataframe-using-googles-api-v4-2020-f50e84ea4530

import os
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#pip install gspread oauth2client
# pip install -r requirements.txt

# products=client.open("Items").sheet1

load_dotenv()

DOCUMENT_ID = os.getenv("GOOGLE_SHEET_ID", default="OOPS")
SHEET_NAME = os.getenv("SHEET_NAME", default="Products-2021")

# AUTHORIZATION
# see: https://gspread.readthedocs.io/en/latest/api.html#gspread.authorize

# an OS-agnostic (Windows-safe) way to reference the "auth/google-credentials.json" filepath:
#CREDENTIALS_FILEPATH = os.path.join(os.path.dirname(__file__), "auth", "google-credentials.json")
#  CODE errored - was looking in the amaconda env folder, not thw ~/Desktop/ one... FIX BUG!!!
CREDENTIALS_FILEPATH = '\\auth\\google-credentials.json'

AUTH_SCOPE = [
#    "https://www.googleapis.com/auth/spreadsheets", #> Allows read/write access to the user's sheets and their properties.
    "https://www.googleapis.com/auth/drive.file" #> Per-file access to files created or opened by the app.
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILEPATH, AUTH_SCOPE)
print("CREDS:", type(credentials)) #> <class 'oauth2client.service_account.ServiceAccountCredentials'>

client = gspread.authorize(credentials)
print("CLIENT:", type(client)) #> <class 'gspread.client.Client'>


def to_usd(my_price):
    return f"${my_price:,.2f}" #> $12,000.71
