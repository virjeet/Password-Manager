import json
from cryptography.fernet import Fernet
import getpass
import secrets
import string

# Encrypt password
def encrypt_password(key, password):
    encrypted_password = Fernet(key)# 
    return encrypted_password.encrypt(password.encode())

# Decrypt password
def decrypt_password(key, encrypted_password):
    decrypted_password = Fernet(key)
    return decrypted_password.decrypt(encrypted_password).decode()

# Generate a strong password
def generate_strong_password(length=16):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for i in range(length))#secret module choses random character and join method joins the randomly selectled characters

# Load stored passwords (JSON format)
def load_passwords(file='passwords.json'):
    try:
        with open(file, 'r') as f:    #we are opening a file in read mode allice f and using load function from json module we are loading contains of the file and returning
            return json.load(f)
    except FileNotFoundError:# if the file does not exists the error is taken care of using except block and return empty dictionary
        return {}


# Save passwords to file (JSON format)
def save_passwords(passwords, file='passwords.json'):
    with open(file, 'w') as f: # we are opening a file in write mode if the file does not exist it will create a new json file but won't give error as it is open in write mode
        json.dump(passwords, f) #here we are saving the passwords using dump fucntion from json module 

# Add a new password
def add_password(key, account, username, password):
    passwords = load_passwords()# here we are loading all the passwords stored previously of differnt accounts from json file
    encrypted_password = encrypt_password(key, password)#we are sending the normal password to the encrypte function to encrypte the given password
    passwords[account] = {'username': username, 'password': encrypted_password.decode()}#here we wre storing the password in the format of like {instagram}:{username:password} dictionary into dictionary 
    save_passwords(passwords)#after adding the password we are sending it to the save function where our password will be stored in json file in form of key value pair

#update password
def update_password(key):
    account = input("Enter the account for which you want to update the password: ")
    passwords = load_passwords()
    
    if account in passwords:
        username = input("Enter the new username of the account (press Enter to keep current): ")
        if username.strip() == '':#username.strip(), it removes any such whitespace from the beginning and end of the username.
            username = passwords[account]['Username']
        
        new_password = getpass.getpass("Enter the new password for the account: ")
        encrypted_password = encrypt_password(key, new_password)
        
        passwords[account] = {"Username": username, "Password": encrypted_password.decode()}
        save_passwords(passwords)
        print("Password updated successfully.")
    else:
        print("Account not found.")


# View all passwords
def view_passwords(key):
    passwords = load_passwords()#here we are loading all the passwords stored previously of differnt accounts from json file
    #password is a dictionary that stores account information 
    #Each key in passwords is an account name (like "Google", "Facebook"), and the value is another dictionary with keys like "username" and "password".
    for account, info in passwords.items():#password.items() Iterates over the dictionary passwords, returning each account and its info (a nested dictionary with username and encrypted password)
        print(f"Account: {account}")
        print(f"Username: {info['username']}")
        print(f"Password: {decrypt_password(key, info['password'].encode())}")#The passwords are stored in an encrypted format, and the decrypt_password function is used to decrypt them using a secure key.

# Main function

master_password = getpass.getpass("Enter master password: ")
key = Fernet.generate_key()  # In practice, you'd derive the key from the master password
#menu driven function 
while True:
    print("\n1. Add Password\n2. View Passwords\n3. Generate Strong Password\n4. update password\n5. exit")
    choice = input("Choose an option: ")

    if choice == '1':
        account = input("Enter platform name of which u want to store password of: ")
        username = input("Enter username of the platform: ")
        password = getpass.getpass("Enter password: ")
        add_password(key, account, username, password)
    elif choice == '2':
        view_passwords(key)
    elif choice == '3':
        print(f"Generated Password: {generate_strong_password()}")
    elif choice == '4':
        update_password(key)
    else:
        break

#git init
#git add .
#git commit -m "message done"
#git branch -M main (if its master)
#git remote add origin link of github repository
#git push -u main