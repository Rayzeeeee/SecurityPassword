import random # Random parameter
import string  # String parameters (lowercase letter, special letter ...)
import pymysql # mysql and python


def database_add_account():
    global database
    try:
        database = pymysql.connect(host="localhost",
                              user="root",
                              password="",
                              database="securepassword")  # Database connection
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
        cursor_add_password = database.cursor()

        cursor_add_password.execute("SELECT * FROM password_gestion WHERE Username=%s AND Plateforme=%s", (verification_username, Add))

        cursor_add_password.execute("INSERT INTO password_gestion (Username, Plateforme, Password) VALUES (%s, %s, %s)",
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
        cursor_view = database.cursor()

        cursor_view.execute(f"SELECT Plateforme, Password FROM password_gestion WHERE Username= %s AND Plateforme= %s", (verification_username, Search))
        view = cursor_view.fetchall() # stocker la valeur de la table à la position Plateforme et Password en fonction du compte et de ce qu'il y a été taper dans le choix de la recherche

        
        if(view):
            for plateforme, password_data in view:
                print(f"The password for {plateforme} is : {password_data}")
            Choice_option()
        else:
            print("Pas de mot de passe pour cette plateforme")
            Choice_option()


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

def delete_password_sql():
    try:
        database = pymysql.connect(host="localhost",
                              user="root",
                              password="",
                              database="securepassword")  # Connexion à la base de données
        cursor_delete_password = database.cursor()
        
        cursor_delete_password.execute(f"DELETE FROM password_gestion WHERE Plateforme=%s", (delete_entry))
        cursor_delete = cursor_delete_password.fetchone()
        print(f"Deleted success for {cursor_delete} !")
        Choice_option()

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
    choice = input("Would you like to add a password or view a password? (Add / View / Delete)")

    if (choice=="Add"):
       Add_password() # Call Add_password function

    if(choice=="View"):
       View_password() # Call View_password function

    if(choice=="Delete"):
        delete_password() # Call Delete_password function


# View password
def View_password():
    global Search
    Search = input("What password search ?")

    database_view_password() # Call Verification function

def delete_password():
    global delete_entry
    delete_entry = input("Quelle mot de passe de plateforme voulez-vous supprimer ?")
    delete_password_sql()
        

#Add password
def Add_password():
    global Add
    global password
    Add = input("Enter the website or application :") 

    alphabet_min = string.ascii_letters + string.punctuation # The character of password is all letters and punctuation

    password = ''.join(random.choice(alphabet_min) for i in range(1, 15)) # Randomization of the password
    
    database_add_password() # Call Verification function
    

Initialize()