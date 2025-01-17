import random
import string

password_list = {} # Create password dictionnary

# Create profil
def Initialize():
    global password
    global PIN
    password = input("Enter a password :")
    PIN = int(input("Enter a PIN :"))
    
    print("Account was created !\n-----------------------------------------------")
    Verification() # Call Verification function

#Verification profil
def Verification():
    verification_password = input("Enter your password :")
    verification_PIN = int(input("Enter your PIN :"))

    if(verification_password==password):
        if(verification_PIN==PIN):
            Choice_option()
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
    Add = input("Enter the website or application :") 

    alphabet_min = string.ascii_letters + string.punctuation # The character of password is all letters and punctuation

    password = ''.join(random.choice(alphabet_min) for i in range(1, 15)) # Randomization of the password
    print(f"The password for {Add} is : {password}")
        
    password_list[Add] = password # Add a argument at the list

    Verification() # Call Verification function
    

Initialize()