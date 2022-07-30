#Prof connect

import os
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

#pip install gspread oauth2client
# pip install -r requirements.txt

# products=client.open("Items").sheet1

load_dotenv()

DOCUMENT_ID = os.getenv("GOOGLE_SHEET_ID", default="1Cj7pfKWXZjLf2b_fwuYioMIq_S4e1zh7yaUeHZfyEiw")
READ_SHEET = os.getenv("PRODUCTS_SHEET_NAME", default="Items")
WRITE_SHEET = os.getenv("RECORDS_SHEET_NAME", default="Transactions")

# AUTHORIZATION
# see: https://gspread.readthedocs.io/en/latest/api.html#gspread.authorize

# an OS-agnostic (Windows-safe) way to reference the "auth/google-credentials.json" filepath:
CREDENTIALS_FILEPATH = os.path.join(os.path.dirname(__file__), "auth", "google-credentials.json")

AUTH_SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets", #> Allows read/write access to the user's sheets and their properties.
    "https://www.googleapis.com/auth/drive.file" #> Per-file access to files created or opened by the app.
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILEPATH, AUTH_SCOPE)
# print("CREDS:", type(credentials)) #> <class 'oauth2client.service_account.ServiceAccountCredentials'>

client = gspread.authorize(credentials)
# print("CLIENT:", type(client)) #> <class 'gspread.client.Client'>


# access the document:
# doc = client.open_by_key(DOCUMENT_ID)
# print("DOC:", type(doc), doc.title) #> <class 'gspread.models.Spreadsheet'>

# access a sheet within the document:
# sheet = doc.worksheet(READ_SHEET)
# print("SHEET:", type(sheet), sheet.title)#> <class 'gspread.models.Worksheet'>

# fetch all data from that sheet:
# rows = sheet.get_all_records()
# print("ROWS:", type(rows)) #> <class 'list'>

# loop through and print each row, one at a time:
# for row in rows:
#     print(row) #> <class 'dict'>

