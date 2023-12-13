from ecdsa.keys import NIST192p
from hashlib import sha256
from ecdsa.util import sigencode_der, sigdecode_der
from ecdsa import SigningKey, VerifyingKey, BadSignatureError

class EncryptDecrypt:
    def __init__(self):
        self.privateKey = None
        self.publicKey = None

    def generatePrivatePublicKeys(self):
        self.privateKey = SigningKey.generate(curve=NIST192p)
        self.publicKey = self.privateKey.get_verifying_key()
        return self.privateKey, self.publicKey

    def savePrivateKey(self):
        with open("privateKey.pem", "wb") as f:
            f.write(self.privateKey.to_pem(format="pkcs8"))

    def savePublicKey(self):
        with open("publicKey.pem", "wb") as f:
            f.write(self.publicKey.to_pem())

    def encryptFile(self):
        with open("text.txt", "rb") as file:
            inputText = file.read()

        encryptedText = self.privateKey.sign_deterministic(
            inputText,
            hashfunc=sha256,
            sigencode=sigencode_der
        )

        with open("encryptedFile.txt", "wb") as opFile:
            opFile.write(encryptedText)

        print(f"\nEncrypted text: {encryptedText}")

    def decryptFile(self):
        with open("text.txt", "r") as file:
            originalData = file.read().encode("utf-8")

        with open("encryptedFile.txt", "rb") as encFile:
            encrypted = encFile.read()

        try:
            self.publicKey.verify(
                encrypted, originalData,
                hashfunc=sha256,
                sigdecode=sigdecode_der
            )

            decryptedText = "Verification successful"

            with open("decryptedFile.txt", "w") as opFile:
                opFile.write(decryptedText)

            print(f"\nDecrypted text: {decryptedText}")

        except BadSignatureError:
            print("Incorrect Signature")

def main():
    print("\nWelcome to Kartik's Encryption-Decryption Services!")
    encDec = EncryptDecrypt()

    with open("text.txt", "w") as file:
        file.write("Om Namo Bhagavate Vasudevaya!")

    encDec.generatePrivatePublicKeys()
    encDec.savePrivateKey()
    encDec.savePublicKey()
    encDec.encryptFile()
    encDec.decryptFile()

    print("\nThank you for using Kartik's Encryption-Decryption Services!\nHope it helped")

if __name__ == "__main__":
    main()
