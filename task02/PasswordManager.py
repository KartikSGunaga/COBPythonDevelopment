import random as rd
import string as st
from ecdsa import SigningKey, NIST256p, BadSignatureError
from hashlib import sha256
from ecdsa.util import sigencode_der, sigdecode_der

class PasswordGenerator:
    def __init__(self):
        self.passwordList = []

    def generatePassword(self, length, numLength, spCharLength,
                         upperCaseLength, lowerCaseLength):
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
        self.passwordList.append({"username": userName,
                              "Password": password})

    def specifyPasswordLength(self):
        choice = input("\nDo you wish to define password length?(yes or no): ")

        if choice == "yes":
            length = int(input("\nEnter the password length: "))
            numLength = int(input(f"\nEnter the number of digits you want({length} chars remaining): "))
            spCharLength = int(input(f"\nEnter the number of digits you want({length - numLength} chars remaining): "))
            upperCaseLength = int(input(f"\nEnter the number of digits you want({length - numLength - spCharLength} chars remaining): "))
            lowerCaseLength = length - spCharLength - upperCaseLength - numLength

        else:
            length = 17
            numLength = rd.randint(1, length - 3)
            spCharLength = rd.randint(1, length - numLength - 2)
            upperCaseLength = rd.randint(1, length - numLength - spCharLength - 1)
            lowerCaseLength = length - spCharLength - upperCaseLength - numLength

        return length, numLength, spCharLength,upperCaseLength, lowerCaseLength

    def displayPasswordByUsername(self, username):
        bool = False
        for key, value in self.passwordList:
            if key.lower() == username:
                print(f'\nPassword associated with \"{key}\" is: {value} ')
                bool = True

        if not bool:
            print("\nNo such username available.")

    def displayAllPasswords(self):
        for password in self.passwordList:
            print("\n", password)

class Authenticate:
    def __init__(self, password):
        self.privateKey = SigningKey.generate(curve=NIST256p)
        self.publicKey = self.privateKey.verifying_key
        self.password = password

    # def generateKeyPair(self):
    #     self.privateKey = SigningKey.generate(curve=NIST256p)
    #     self.publicKey = self.privateKey.verifying_key

    def saveKeyPairs(self):
        with open("privateKey.pem","wb") as file:
            file.write(self.privateKey.to_pem(format="pkcs8"))

        with open("publicKey.pem", "wb") as file:
            file.write(self.publicKey.to_pem(format="pkcs8"))
    def encryptPassword(self):
        encryptedPassword = self.publicKey.sign_deterministic(
            self.password,
            hashfunc=sha256,
            sigencode=sigencode_der
        )
        return encryptedPassword

    def decryptPassword(self, encryptedPassword):
        decryptedPassword = self.privateKey.verify(encryptedPassword,
                                                   self.password,
                                                   sha256,
                                                   sigdecode=sigdecode_der)

        try:
            # ret = self.privateKey.verify(decryptedPassword, self.password, sha256, sigdecode=sigdecode_der)
            assert decryptedPassword
            print("Valid signature")
        except BadSignatureError:
            print("Incorrect signature")

        return decryptedPassword

def menu():
    print("\n  Menu\n"
          "1. Generate Password \n"
          "2. View stored passwords \n"
          "3. Retrieve password by username\n"
          "4. Exit")

def authenticate(password):
    user = Authenticate(password)
    encryptData = user.encryptPassword()

    return user.decryptPassword(encryptData)

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