# IMPORTS
import datetime
import os
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


# LOAD ENVIROMENT VARS & DATA SECTION
load_dotenv()
tax_rate = float((os.getenv('TAX_RATE')))
DOCUMENT_ID = os.getenv("GOOGLE_SHEET_ID", default="secured")
READ_SHEET = os.getenv("PRODUCTS_SHEET_NAME", default="secured")
WRITE_SHEET = os.getenv("RECORDS_SHEET_NAME", default="secured")
EMAILS_SHEET = os.getenv("EMAILS_SHEET_NAME", default="secured")

# AUTHORIZATION - code from Prof
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
emails_sheet = doc.worksheet(EMAILS_SHEET)

products = read_sheet.get_all_records()

# USD CLEANUP BIT - Code from Prof
def to_usd(my_price):
    return f"${my_price:,.2f}" #> $12,000.71

# OTHER SETUP THINGS
escape = ["X", "DONE"]  # User options to break out of loop - so program is more intuitive to more people!
yes = ["Y", "YES"]  #  So user can answer yes with y or yes
# tax_rate = 0.0875  # ENVIROMENT VARIABLE NOW

#PROGRAM LOOP POINT FOR MULTIPLE CUSTOMERS
while True:
# PROGRAM START - things that have to happen each loop
    checkout_time = datetime.datetime.now() # https://www.w3schools.com/python/python_datetime.asp
    subtotal_price = 0
    selected_products = [] 
    email_purchases = ""  #clear the string for the next customer
    print("Please input a product ID, or press 'X' to finalize checkout.")

# ENTER ITEMS LOOP SECTION - Code from Prof
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
    print("www.shoppingcart.zacharyspitzer.com")
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


# TEXT FILE RECIEPT CREATION - code adapted from prof, google, and stack overflow
    make_rcpt = input("Generate Text Reciept to print? (y/n): ")
    if make_rcpt.upper() in yes:
        filenametime = timestr = checkout_time.strftime("Reciept_%Y_%m_%d-%H%M%S.txt")
        rcpt = open(os.path.join(os.path.dirname(__file__), "reciepts", filenametime), "x")
        rcpt.write("        Corner Store Bodega""\n""83rd & West End, NYC | 212.671.4602""\n""www.shoppingcart.zacharyspitzer.com""\n""\n""Your Purchases:""\n")
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

#EMAIL RECIEPT SECTION - code adapted from prof
    email_rcpt = input("eMail Reciept? (y/n): ")
    if email_rcpt.upper() in yes: 
        email_checkout_time = timestr = checkout_time.strftime("%I:%M:%S %p")
        customer_email = input("Enter customer email address: ")
        SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", default="OOPS, please set env var called 'SENDGRID_API_KEY'")
        SENDER_ADDRESS = os.getenv("SENDER_ADDRESS", default="OOPS, please set env var called 'SENDER_ADDRESS'")
        SENDGRID_TEMPLATE_ID = os.getenv("SENDGRID_TEMPLATE_ID", default="OOPS, please set env var called 'SENDGRID_TEMPLATE_ID'")
        for purchase in selected_products:
            email_purchases = email_purchases+("<li>"+purchase["name"]+" ("+to_usd(purchase["price"])+")</li>")

        email_template_data = {
            "google_checkout_date":google_checkout_date,
            "google_checkout_time":email_checkout_time,
            "tax":to_usd(tax),
            "subtotal_price":to_usd(subtotal_price),
            "grandtotal_price":to_usd(grandtotal_price),
            "purchases":email_purchases
        }

        client = SendGridAPIClient(SENDGRID_API_KEY)
        # print("CLIENT:", type(client))

        message = Mail(from_email=SENDER_ADDRESS, to_emails=customer_email)
        message.template_id = SENDGRID_TEMPLATE_ID
        message.dynamic_template_data = email_template_data
        # print("MESSAGE:", type(message))

        try:
            response = client.send(message)
            # print("RESPONSE:", type(response)) #> <class 'python_http_client.client.Response'>
            # print(response.status_code) #> 202 indicates SUCCESS
            # print(response.body)
            # print(response.headers)

        except Exception as err:
            print(type(err))
            print(err)

    # SAVE EMAIL ADDRESS TO GOOGLE SHEET FOR MARKETING - adapted from above code adapted from Prof
        save_email = input("Add customer to email list? (y/n): ")
        if save_email.upper() in yes:
            new_email_row = {
                "date":google_checkout_date,
                "time":google_checkout_time,
                "email address":customer_email
            }
            new_email_values = list(new_email_row.values()) 
            rows_email = emails_sheet.get_all_records()
            next_email_row_number = len(rows_email) + 2
            response_email = emails_sheet.insert_row(new_email_values, next_email_row_number)

# ANOTHER CUSTOMER? TO LOOP OR NOT TO LOOP, THAT IS THE QUESTION?
    next_customer = input("Check out next customer? (y/n): ")
    if next_customer.upper() not in yes:
        print("")
        print("Thanks for being a great employee!")
        print("")
        break

