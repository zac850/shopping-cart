# for how to connect google & python:
# https://developers.google.com/sheets/api/quickstart/python 
# https://towardsdatascience.com/how-to-import-google-sheets-data-into-a-pandas-dataframe-using-googles-api-v4-2020-f50e84ea4530

# IMPORTS
import datetime #https://thispointer.com/add-minutes-to-current-time-in-python/


# DATA SECTION

products = [
    {"id":1, "name": "Chocolate Sandwich Cookies", "department": "snacks", "aisle": "cookies cakes", "price": 3.50},
    {"id":2, "name": "All-Seasons Salt", "department": "pantry", "aisle": "spices seasonings", "price": 4.99},
    {"id":3, "name": "Robust Golden Unsweetened Oolong Tea", "department": "beverages", "aisle": "tea", "price": 2.49},
    {"id":4, "name": "Smart Ones Classic Favorites Mini Rigatoni With Vodka Cream Sauce", "department": "frozen", "aisle": "frozen meals", "price": 6.99},
    {"id":5, "name": "Green Chile Anytime Sauce", "department": "pantry", "aisle": "marinades meat preparation", "price": 7.99},
    {"id":6, "name": "Dry Nose Oil", "department": "personal care", "aisle": "cold flu allergy", "price": 21.99},
    {"id":7, "name": "Pure Coconut Water With Orange", "department": "beverages", "aisle": "juice nectars", "price": 3.50},
    {"id":8, "name": "Cut Russet Potatoes Steam N' Mash", "department": "frozen", "aisle": "frozen produce", "price": 4.25},
    {"id":9, "name": "Light Strawberry Blueberry Yogurt", "department": "dairy eggs", "aisle": "yogurt", "price": 6.50},
    {"id":10, "name": "Sparkling Orange Juice & Prickly Pear Beverage", "department": "beverages", "aisle": "water seltzer sparkling water", "price": 2.99},
    {"id":11, "name": "Peach Mango Juice", "department": "beverages", "aisle": "refrigerated", "price": 1.99},
    {"id":12, "name": "Chocolate Fudge Layer Cake", "department": "frozen", "aisle": "frozen dessert", "price": 18.50},
    {"id":13, "name": "Saline Nasal Mist", "department": "personal care", "aisle": "cold flu allergy", "price": 16.00},
    {"id":14, "name": "Fresh Scent Dishwasher Cleaner", "department": "household", "aisle": "dish detergents", "price": 4.99},
    {"id":15, "name": "Overnight Diapers Size 6", "department": "babies", "aisle": "diapers wipes", "price": 25.50},
    {"id":16, "name": "Mint Chocolate Flavored Syrup", "department": "snacks", "aisle": "ice cream toppings", "price": 4.50},
    {"id":17, "name": "Rendered Duck Fat", "department": "meat seafood", "aisle": "poultry counter", "price": 9.99},
    {"id":18, "name": "Pizza for One Suprema Frozen Pizza", "department": "frozen", "aisle": "frozen pizza", "price": 12.50},
    {"id":19, "name": "Gluten Free Quinoa Three Cheese & Mushroom Blend", "department": "dry goods pasta", "aisle": "grains rice dried goods", "price": 3.99},
    {"id":20, "name": "Pomegranate Cranberry & Aloe Vera Enrich Drink", "department": "beverages", "aisle": "juice nectars", "price": 4.25}
] # based on data from Instacart: https://www.instacart.com/datasets/grocery-shopping-2017

# USD CLEANUP BIT
def to_usd(my_price):
    return f"${my_price:,.2f}" #> $12,000.71

# OTHER SETUP THINGS
selected_products = [] 
escape = ["X", "DONE"]  # User options to break out of loop - so program is more intuitive to more people!
subtotal_price = 0
tax_rate = 0.0875  # MAKE ENVIROMENT VARIABLE!
checkout_time = datetime.datetime.now() # https://www.w3schools.com/python/python_datetime.asp

# PROGRAM START
#tax_rate = input("Enter tax rate (0.0875 for NYC): ")
#tax_rate = float(tax_rate)
print("Please input a product ID, or press 'X' to finalize checkout.")

# ENTER ITEMS LOOP SECTION
while True:
    selected_id = input("  ID (or x): " )

    if selected_id.upper() in escape:
        break # break out of the while loop 
    else:
        matching_products = [p for p in products if str(p["id"]) == str(selected_id)]
        matching_product = matching_products[0] # BUG this will trigger an IndexError if there are no matching products
        selected_products.append(matching_product)
        subtotal_price = subtotal_price + matching_product["price"]
 

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
