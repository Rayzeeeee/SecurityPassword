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
            Choice_option()

    except Exception as es:
        print(f"Erreur de connexion : {str(es)}")

def database_add_password():
    try:
        cursor = database.cursor()

        cursor.execute("SELECT * FROM password gestion WHERE Plateforme=%s", (Add,))
        row = cursor.fetchone()
        
        if row is not None:
            print("Plateforme déjà utilisé")
        else:
            cursor.execute("INSERT INTO password_gestion (Plateforme, Password) VALUES (%s, %s)",
                        (verification_username, Add, password))
            database.commit()
            print("Ajout effectué !")
            Verification()
        
    except Exception as es:
        print(f"Erreur de connexion : {str(es)}")



# Create profil
def Initialize():
    create_sign = input("Create or Sign-up ?")
    if(create_sign=="Create"):
        Create()
    if(create_sign=="Sign-up"):
        Verification()

def Create():
    global username
    global PIN
    global password_entry
    username = input("Enter a username : ")
    password_entry = input("Enter a password :")
    PIN = int(input("Enter a PIN :"))
    
    print("Account was created !\n-----------------------------------------------")
    Verification() # Call Verification function

#Verification profil
def Verification():
    global verification_username
    global verification_PIN
    global verification_password_entry
    verification_username = input("Enter your username :")
    verification_password_entry = input("Enter your password :")
    verification_PIN = int(input("Enter your PIN :"))

    if verification_username==username:
        if(verification_password_entry==password_entry):
            if(verification_PIN==PIN):
                database_add_account()
            else:
                print("Incorrect password !")

# Choice option
def Choice_option():
    choice = input("Would you like to add a password or view a password? (Add / View)")

    if (choice=="Add"):
       Add_password() # Call Add_password function

    if(choice=="View"):
       View_password() # Call View_password function


# View password
def View_password():
    Search = input("What password search ?")

    if(Search in password_list):
        the_password = password_list.get(Search)
        print(f"The password for {Search} is : {the_password}")
        Verification() # Call Verification function
    else:
        print(f"No password is register in {Search}")
        Verification() # Call Verification function
        

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