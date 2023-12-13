# Importing necessary modules
import random as rd
import string as st
from ecdsa import SigningKey, NIST256p, BadSignatureError
from hashlib import sha256
from ecdsa.util import sigencode_der, sigdecode_der

# Class to generate and manage passwords
class PasswordGenerator:
    def __init__(self):
        self.passwordList = []  # List to store generated passwords

    # Method to generate a random password based on specified criteria
    def generatePassword(self, length, numLength, spCharLength, upperCaseLength, lowerCaseLength):
        count = 0
        password = ""
        userName = input("\nEnter the username you wish to associate the password with: ")
        while count < length:
            randomChoice = rd.choice(["num","spChar","lowerCase","upperCase"])

            if randomChoice == "num" and numLength > 0:
                password += rd.choice(st.digits)
                count += 1
            elif randomChoice == "spChar" and spCharLength > 0:
                password += rd.choice(st.punctuation)
                count += 1
            elif randomChoice == "upperCase" and upperCaseLength > 0:
                password += rd.choice(st.ascii_uppercase)
                count += 1
            elif randomChoice == "lowerCase" and lowerCaseLength > 0:
                password += rd.choice(st.ascii_lowercase)
                count += 1

        print(f"The recommended password is: {password}")
        self.passwordList.append({"username": userName, "Password": password})

    # Method to specify the length of the password based on user input
    def specifyPasswordLength(self):
        choice = input("\nDo you wish to define password length?(yes or no): ")

        if choice == "yes":
            length = int(input("\nEnter the password length: "))
            numLength = int(input(f"\nEnter the number of digits you want({length} chars remaining): "))
            spCharLength = int(input(f"\nEnter the number of special characters you want({length - numLength} chars remaining): "))
            upperCaseLength = int(input(f"\nEnter the number of uppercase characters you want({length - numLength - spCharLength} chars remaining): "))
            lowerCaseLength = length - spCharLength - upperCaseLength - numLength

        else:
            length = 17
            numLength = rd.randint(1, length - 3)
            spCharLength = rd.randint(1, length - numLength - 2)
            upperCaseLength = rd.randint(1, length - numLength - spCharLength - 1)
            lowerCaseLength = length - spCharLength - upperCaseLength - numLength

        return length, numLength, spCharLength, upperCaseLength, lowerCaseLength

    # Method to display a password associated with a specific username
    def displayPasswordByUsername(self, username):
        found = False
        for entry in self.passwordList:
            if entry["username"].lower() == username.lower():
                print(f'\nPassword associated with \"{entry["username"]}\" is: {entry["Password"]} ')
                found = True

        if not found:
            print("\nNo such username available.")

    # Method to display all stored passwords
    def displayAllPasswords(self):
        for password in self.passwordList:
            print("\n", password)

# Class to handle authentication and password encryption/decryption
class Authenticate:
    def __init__(self, password):
        self.privateKey = SigningKey.generate(curve=NIST256p)
        self.publicKey = self.privateKey.verifying_key
        self.password = password

    # Method to save generated private and public key pairs to files
    def saveKeyPairs(self):
        with open("privateKey.pem", "wb") as file:
            file.write(self.privateKey.to_pem(format="pkcs8"))

        with open("publicKey.pem", "wb") as file:
            file.write(self.publicKey.to_pem(format="pkcs8"))

    # Method to encrypt a password using private key
    def encryptPassword(self):
        encryptedPassword = self.privateKey.sign_deterministic(
            self.password,
            hashfunc=sha256,
            sigencode=sigencode_der
        )
        return encryptedPassword

    # Method to decrypt an encrypted password using public key
    def decryptPassword(self, encryptedPassword):
        decryptedPassword = self.publicKey.verify(encryptedPassword,
                                                  self.password,
                                                  sha256,
                                                  sigdecode=sigdecode_der)

        try:
            assert decryptedPassword
            print("Valid signature")
        except BadSignatureError:
            print("Incorrect signature")

        return decryptedPassword

# Method to display the menu options
def menu():
    print("\n  Menu\n"
          "1. Generate Password \n"
          "2. View stored passwords \n"
          "3. Retrieve password by username\n"
          "4. Exit")

# Method to authenticate the user and perform actions based on menu choice
def authenticate(password):
    user = Authenticate(password)
    encryptData = user.encryptPassword()

    return user.decryptPassword(encryptData)

# Main method to run the password manager
def main():
    print("\nWelcome to Kartik's Password Manager!")
    menu()
    passkey = PasswordGenerator()

    while True:
        choice = int(input("\nEnter your choice(5 to view menu): "))

        try:
            if choice == 1:
                length, numLength, spChars, upperCases, lowerCases = passkey.specifyPasswordLength()
                passkey.generatePassword(length, numLength, spChars, upperCases, lowerCases)

            elif choice == 2:
                password = input("\nEnter the password: ")
                if authenticate(password):
                    passkey.displayAllPasswords()
                else:
                    print("\nPassword mismatch! \n"
                          "Please try again.")

            elif choice == 3:
                password = input("\nEnter the password: ")
                if authenticate(password):
                    username = input("\nEnter the username of the password you wish to search: ")
                    passkey.displayPasswordByUsername(username)
                else:
                    print("\nPassword mismatch! \n"
                          "Please try again.")

            elif choice == 4:
                print("\nThank you for using Kartik's Password Manager! \n"
                      "Hope it helped!")
                break

        except ValueError:
            print("\nBad choice. Please input integers between 1-5.")

if __name__ == "__main__":
    main()
