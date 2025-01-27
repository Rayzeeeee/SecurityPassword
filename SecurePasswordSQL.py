import random # Random parameter
import string  # String parameters (lowercase letter, special letter ...)
import pymysql # mysql and python

database = pymysql.connect(host="localhost",
                              user="root",
                              password="",
                              database="securepassword")  # Connecting to the database

# Add account function sql
def database_add_account():
    global database
    try:
        cursor = database.cursor() # Create a cursor in the database

        cursor.execute("SELECT * FROM accounts WHERE Username=%s", (username,)) # Select all in "accounts" in Username
        row = cursor.fetchone()

        # Check if the username already exists
        if row is not None:
            print("Existing username")
        else:
            # Adding data in the database
            cursor.execute("INSERT INTO accounts (Username, Password, PIN) VALUES (%s, %s, %s)", (username, password_entry, PIN)) # Insert into accounts values(Username, Password and PIN)
            database.commit() # Add in the database
            Initialize()

    except Exception as es:
        # Error message
        print(f"Connection error : {str(es)}")

# Add password function sql
def database_add_password():
    try:
        cursor_add_password = database.cursor() # Create a cursor in the database

        cursor_add_password.execute("SELECT * FROM password WHERE Username=%s AND Platform=%s", (check_username, Add)) # Select all in "password" in values of Username and Platform

        cursor_add_password.execute("INSERT INTO password (Username, Platform, Password) VALUES (%s, %s, %s)", (check_username, Add, password)) # Insert into password values (Username, Platform and Password)
        database.commit() # Add in the database
        print("Password created !")
        Choice_option() # Return to the choice_option
        
    except Exception as es:
        # Error message
        print(f"Connection error : {str(es)}")

# View password function sql
def database_view_password():
    try:
        cursor_view = database.cursor() # Create a cursor in the database

        cursor_view.execute(f"SELECT Platform, Password FROM password WHERE Username= %s AND Platform= %s", (check_username, Search)) # Select Platform and Password in password in Username and Platform values
        view = cursor_view.fetchall() # stock all the result of the select 

        if(view):
            for platforme, password_data in view:
                print(f"The password for {platforme} is : {password_data}") # Show the platform and password
            Choice_option()
        else:
            # Error message
            print("No password for the platform")
            Choice_option() # Return to the choice_option


    except Exception as es:
        # Error message for the database 
        print(f"Connection error : {str(es)}")

# Connect account function sql
def database_connect():
    try:

        cursor_connect_username = database.cursor() # Create a cursor in the database
        cursor_connect_password = database.cursor() 
        cursor_connect_PIN = database.cursor()

        # Select all in the account in Username, Password and PIN
        sql_connect_username = (f"SELECT * FROM accounts WHERE Username= '{check_username}' ")
        sql_connect_password = (f"SELECT * FROM accounts WHERE Password= '{check_password}' ")
        sql_connect_PIN = (f"SELECT * FROM accounts WHERE PIN= '{check_PIN}' ")

        cursor_connect_username.execute(sql_connect_username)
        cursor_username = cursor_connect_username.fetchone()

        cursor_connect_password.execute(sql_connect_password)
        cursor_password = cursor_connect_password.fetchone()

        cursor_connect_PIN.execute(sql_connect_PIN)
        cursor_PIN = cursor_connect_PIN.fetchone()

        # if the values correspond to a account
        if(check_username in cursor_username):
           if(check_password in cursor_password):
             if(check_PIN in cursor_PIN):  
                print("Successfully connected !")
                Choice_option() # Return to the choice_option
        else:
            # Error message
            print("Account not existed")
    except Exception as es:
        # Error message sql
        print(f"Connection error : {str(es)}")

# Delete password function sql
def delete_password_sql():
    try:
        cursor_delete_password = database.cursor() # Create a cursor in the database
        
        cursor_delete_password.execute(f"DELETE FROM password WHERE Platform=%s", (delete_entry)) # Delete in password the values plateform
        database.commit() # Add in the database
        
        print("Successfully delete !")
        Choice_option() # Return to the choice_option

    except Exception as es:
        # Error message sql
        print(f"Connection error : {str(es)}")

# -----------------------------------------------------------------------------------------------------------

# Create profil
def Initialize():
    create_sign = input("Sign-up or Login ?")
    if(create_sign=="Sign-up"): # Sign-up -> Create_account function
        Create_account()
    if(create_sign=="Login"): # Sign-up -> Connect function
        Connect()

# Create account 
def Create_account():
    global username
    global PIN
    global password_entry
    # Entry for create
    username = input("Enter a username : ")
    password_entry = input("Enter a password :")
    PIN = int(input("Enter a PIN (max 4 : integer):"))
    
    print("Account was created !\n-----------------------------------------------") # Separation
    database_add_account()() # Call Verification function

#Connect to a account
def Connect():
    global check_username
    global check_PIN
    global check_password
    check_username = input("Enter your username :")
    check_password = input("Enter your password :")
    check_PIN = int(input("Enter your PIN :"))
    database_connect()

# Choice option
def Choice_option():
    choice = input("Would you like to add a password or view a password? (Add / View / Delete)") # Choice option entry

    if (choice=="Add"):
       Add_password() # Call Add_password function

    if(choice=="View"):
       View_password() # Call View_password function

    if(choice=="Delete"):
        Delete_password() # Call Delete_password function


# View password
def View_password():
    global Search
    Search = input("What password search ?")

    database_view_password() # Call Verification function

# Delete password
def Delete_password():
    global delete_entry
    delete_entry = input("Which password do you want to delete ?") # Delete password entry
    delete_password_sql()
        

#Add password
def Add_password():
    global Add
    global password
    Add = input("Enter the website or application :") # Add password entry

    alphabet_min = string.ascii_letters + string.punctuation # The character of password is all letters and punctuation

    password = ''.join(random.choice(alphabet_min) for i in range(1, 15)) # Randomization of the password
    
    database_add_password() # Call Verification function
    
Initialize()