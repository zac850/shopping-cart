# for how to connect google & python:
# https://developers.google.com/sheets/api/quickstart/python 
# https://towardsdatascience.com/how-to-import-google-sheets-data-into-a-pandas-dataframe-using-googles-api-v4-2020-f50e84ea4530

# IMPORTS
import datetime
from tkinter import Y #https://thispointer.com/add-minutes-to-current-time-in-python/
import smtplib, ssl
from email.message import EmailMessage
import os
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# LOAD ENVIROMENT VARS
load_dotenv()
tax_rate = float((os.getenv('TAX_RATE')))


# DATA SECTION
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
client = gspread.authorize(credentials)

doc = client.open_by_key(DOCUMENT_ID)
read_sheet = doc.worksheet(READ_SHEET)
write_sheet = doc.worksheet(WRITE_SHEET)

products = read_sheet.get_all_records()

# USD CLEANUP BIT
def to_usd(my_price):
    return f"${my_price:,.2f}" #> $12,000.71

# OTHER SETUP THINGS
escape = ["X", "DONE"]  # User options to break out of loop - so program is more intuitive to more people!
# tax_rate = 0.0875  # ENVIROMENT VARIABLE NOW


# PROGRAM START - things that have to happen each loop
checkout_time = datetime.datetime.now() # https://www.w3schools.com/python/python_datetime.asp
subtotal_price = 0
selected_products = [] 
print("Please input a product ID, or press 'X' to finalize checkout.")

# ENTER ITEMS LOOP SECTION
while True:
    selected_id = input("  ID (or x): " )

    if selected_id.upper() in escape:
        break  
    else:
        try:
            matching_products = [p for p in products if str(p["id"]) == str(selected_id)]
            matching_product = matching_products[0] 
            selected_products.append(matching_product)
            subtotal_price = subtotal_price + matching_product["price"]

        except IndexError:
            print("Invalid ID - Try Again:")

# DISPLAY ITEMS SECTION
print("-------------------")
print("Corner Store Bodega")
print("83rd & West End, NYC | 212.671.4602")
print("www.shopping_cart.zacharyspitzer.com") # MAKE THIS WEBSITE!!!
print("-------------------")
print("Checkout Time:",(checkout_time.strftime("%a %b %d %Y, %I:%M %p")))  #https://www.w3schools.com/python/python_datetime.asp
print("Purchases:")
for purchase in selected_products:
    print(" *",purchase["name"],"("+to_usd(purchase["price"])+")") 

# CALCULATE TOTAL & PRINT TOTAL SECTION
tax = subtotal_price * tax_rate
grandtotal_price = subtotal_price + tax
print("-------------------")
print("Subtotal:",to_usd(subtotal_price))
print("Tax:",to_usd (tax))
print("Grand Total:", to_usd (grandtotal_price))
print("-------------------")
print("Thank you for your patronage!")
print("-------------------")
print("")

# UPLOAD TRANSACTION FOR ACCOUNTANT - adapted from Prof's code
google_checkout_date = timestr = checkout_time.strftime("%m/%d/%y")
google_checkout_time = timestr = checkout_time.strftime("%H:%M:%S")

new_row = {
    "date":google_checkout_date,
    "time":google_checkout_time,
    "subtotal":to_usd(subtotal_price),
    "tax":to_usd(tax),
    "grand total":to_usd(grandtotal_price)
}
new_values = list(new_row.values()) 
rows = write_sheet.get_all_records()
next_row_number = len(rows) + 2
response = write_sheet.insert_row(new_values, next_row_number)


# TEXT FILE RECIEPT CREATION
make_rcpt = input("Generate Text Reciept to print? (y/n): ")
if make_rcpt.upper() == "Y":
    filenametime = timestr = checkout_time.strftime("Reciept_%Y%m%d-%H%M%S")
    rcpt = open(filenametime, "x")      # BUG Need to get it to put the text files in the reciepts folder, not working dir...
    rcpt.write("Corner Store Bodega""\n""83rd & West End, NYC | 212.671.4602""\n""\n""Your Purchases:""\n")
    for purchase in selected_products:
        rcpt.write(" * ")
        rcpt.write(purchase["name"])
        rcpt.write("  (")
        rcpt.write(to_usd(purchase["price"]))
        rcpt.write(")""\n")
    rcpt.write("\n""-------------------""\n""Subtotal: ")
    rcpt.write(to_usd(subtotal_price))
    rcpt.write("\n""Tax: ")
    rcpt.write(to_usd (tax))
    rcpt.write("\n""Grand Total: ")
    rcpt.write(to_usd (grandtotal_price))
    rcpt.write("\n""-------------------""\n""Thank you for your patronage!""\n""-------------------")
    rcpt.close()   #In the real world, os.startfile"filenametime",print) and then on a linux machine with the folder hirarchy it should print...

# EMAIL RECIEPT  https://docs.python.org/3/library/email.examples.html
# email_rcpt = input("eMail Reciept? (y/n): ")
# if email_rcpt.upper() == "Y":   #https://realpython.com/python-send-email/
#     port = 465
#     smtp_server = 'mail.zacharyspitzer.com'
#     sender_email = 'receipt@zacharyspitzer.com'
#     receiver_email = input("Enter customer email: ")
#     password = "shopping_cart"  # BUG use getpass module / function
#     message = """\
#     Subject: Your Reciept

#     This is a test email. """

#     context = ssl.create_default_context()
#     with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
#         server.login(sender_email, password)
#         server.sendmail(sender_email, receiver_email, message)
