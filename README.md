# Welcome

## Prerequisites
* Anaconda 3.7+
* Python 3.8+

## Setup

First, download (clone) to your desktop

Then, in your command line (e.g. Terminal), create a virtural enviroment (you only need to do this the first time):

 ```sh
 conda create -n shopping-cart python=3.8
 ``` 

Next, activate the virtural enviroment you just made:

 ```sh
 conda activate shopping-cart
 ```

Now navigate to the folder the program download exists in (should be your desktop, if you followed step 1):

 ```sh
cd ~/Desktop/shopping-cart
 ```

Then install the necessary requirments:
```sh
pip install -r requirements.txt
```

### Enviroment Variables
The developer, after signing the contract, will provide a .env file that includes, among other things, the API keys for the google sheet integration, and email integration. This .env folder must be copied into the main shopping_cart folder. 

The developer will also provide a .json file for the google sheet integration. This must be named and located in:
```sh
shopping_cart/auth/google-credentials.json
```

# Operation
To run the program, in your command line, run:
```sh
python cart.py
```

To check out a customer, enter the product ID of the item a customer wishes to purchase, then press ENTER (or return). Continue entering all items the customer wishes to purchase.

When all items are entered, press X (or type done) to generate the reciept. The sub total, tax, and grand total will be displayed on the screen, as well as the items being purchased.

The program will then ask if the customer wants a text reciept to be generated for you to print. Press y to generate this reciept. The reciept will be generated in the shopping_cart/reciepts folder with the checkout date and time as the file name.

The program then asks if the customer wants their reciept emailed. If so, press y, and then enter their email address.

If the customer wants their reciept emailed, the program will then ask for permission to add the customer to the email list. If the customer gives their permission, press y.

That finishes the checkout process. To check out the next customer, press y and continue the same process.

# Administration
This program uses three spreadsheets in one google doc file. The google doc file is:
https://docs.google.com/spreadsheets/d/1Cj7pfKWXZjLf2b_fwuYioMIq_S4e1zh7yaUeHZfyEiw/edit#gid=0

Items available for purchase, their price, department, and aisle, can be modified from the Items sheet.

For accounting records, all transactions are automatically written to the Transactions sheet.

If the customer permits their email address to be added to the email list, it will be added to the customer_emails sheet.

## Tax Rate
To modify the tax rate, open the .env file and modify the line
```sh
TAX_RATE = 0.0875
```
to the correct tax rate. 0.0875 is 8.75%
