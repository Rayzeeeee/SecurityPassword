import random
import string
import pymysql

password_list = {} # Create password dictionnary


def database_add_account():
    global database
    try:
        database = pymysql.connect(host="localhost",
                              user="root",
                              password="",
                              database="securepassword")  # Connexion à la base de données
        cursor = database.cursor()

        # Vérification si l'email existe déjà
        cursor.execute("SELECT * FROM infos WHERE Username=%s", (username,))
        row = cursor.fetchone()

        if row is not None:
            print("Username déjà utilisé")
        else:
            # Insertion des données
            cursor.execute("INSERT INTO infos (Username, Password, PIN) VALUES (%s, %s, %s)",
                        (username, password_entry, PIN))
            database.commit()
            print("Ajout effectué")
            Initialize()

    except Exception as es:
        print(f"Erreur de connexion : {str(es)}")

def database_add_password():
    try:
        database = pymysql.connect(host="localhost",
                              user="root",
                              password="",
                              database="securepassword")  # Connexion à la base de données
        cursor = database.cursor()

        cursor.execute("SELECT * FROM password_gestion WHERE Plateforme=%s", (Add,))
        row = cursor.fetchone()
        
        if row is not None:
            print("Plateforme déjà utilisé")
            row = None
        else:
            cursor.execute("INSERT INTO password_gestion (Username, Plateforme, Password) VALUES (%s, %s, %s)",
                        (verification_username, Add, password))
            database.commit()
            print("Ajout effectué !")
            Choice_option()
        
    except Exception as es:
        print(f"Erreur de connexion : {str(es)}")

def database_view_password():
    try:
        database = pymysql.connect(host="localhost",
                              user="root",
                              password="",
                              database="securepassword")  # Connexion à la base de données
        cursor_plateforme = database.cursor()
        cursor_password = database.cursor()

        cursor_plateforme.execute(f"SELECT Plateforme FROM password_gestion WHERE Plateforme= '{Search}'")
        plateforme = cursor_plateforme.fetchone()

        cursor_password.execute(f"SELECT Password FROM password_gestion WHERE Plateforme= '{Search}'")
        password_data = cursor_password.fetchone()
        
        if(Search in plateforme):
            print(f"The password for {plateforme} is : {password_data}")
            Choice_option()
        else:
            print("Pas de mot de passe pour cette plateforme")


    except Exception as es:
        print(f"Erreur de connexion : {str(es)}")

def database_connect():
    try:
        database = pymysql.connect(host="localhost",
                              user="root",
                              password="",
                              database="securepassword")  # Connexion à la base de données

        cursor_connect_username = database.cursor()
        cursor_connect_password = database.cursor()
        cursor_connect_PIN = database.cursor()

        sql_connect_username = (f"SELECT * FROM infos WHERE Username= '{verification_username}' ")
        sql_connect_password = (f"SELECT * FROM infos WHERE Password= '{verification_password_entry}' ")
        sql_connect_PIN = (f"SELECT * FROM infos WHERE PIN= '{verification_PIN}' ")

        cursor_connect_username.execute(sql_connect_username)
        cursor_username = cursor_connect_username.fetchone()

        cursor_connect_password.execute(sql_connect_password)
        cursor_password = cursor_connect_password.fetchone()

        cursor_connect_PIN.execute(sql_connect_PIN)
        cursor_PIN = cursor_connect_PIN.fetchone()

        if(verification_username in cursor_username):
           if(verification_password_entry in cursor_password):
             if(verification_PIN in cursor_PIN):  
                print("Connexion réussi !")
                Choice_option()
        else:
            print("Account not existed")
    except Exception as es:
        print(f"Erreur de connextion : {str(es)}")


# Create profil
def Initialize():
    create_sign = input("Sign-up or Login ?")
    if(create_sign=="Sign-up"):
        Create()
    if(create_sign=="Login"):
        Verification()

def Create():
    global username
    global PIN
    global password_entry
    username = input("Enter a username : ")
    password_entry = input("Enter a password :")
    PIN = int(input("Enter a PIN :"))
    
    print("Account was created !\n-----------------------------------------------")
    database_add_account()() # Call Verification function

#Verification profil
def Verification():
    global verification_username
    global verification_PIN
    global verification_password_entry
    verification_username = input("Enter your username :")
    verification_password_entry = input("Enter your password :")
    verification_PIN = int(input("Enter your PIN :"))
    database_connect()

# Choice option
def Choice_option():
    choice = input("Would you like to add a password or view a password? (Add / View)")

    if (choice=="Add"):
       Add_password() # Call Add_password function

    if(choice=="View"):
       View_password() # Call View_password function


# View password
def View_password():
    global Search
    Search = input("What password search ?")

    database_view_password() # Call Verification function

        

#Add password
def Add_password():
    global password_list
    global Add
    global password
    Add = input("Enter the website or application :") 

    alphabet_min = string.ascii_letters + string.punctuation # The character of password is all letters and punctuation

    password = ''.join(random.choice(alphabet_min) for i in range(1, 15)) # Randomization of the password
    print(f"The password for {Add} is : {password}")
        
    password_list[Add] = password # Add a argument at the list
    
    database_add_password() # Call Verification function
    

Initialize()