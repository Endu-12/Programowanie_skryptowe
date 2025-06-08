from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2

#Creating a key from Password using Password-Based Key Derivation Function 2
def derive_key(password: str, salt: bytes, key_len: int = 32) -> bytes:
    return PBKDF2(password, salt, dkLen=key_len, count=100000)

#Function responsible for file encryption
def encrypt(password: str, input: str, output: str):
    try:
        #Creating key, salt (from 16 random bytes) and IV (also from 16 random bytes)
        salt = get_random_bytes(16)
        key = derive_key(password, salt)
        iv = get_random_bytes(16)

        #Creating object responsible for encryption in later parts of the program
        cipher = AES.new(key, AES.MODE_CBC, iv)

        #Readind the file we want to Encrypt
        with open(input, "rb") as file:
            data = file.read()

        #Encryption
        padded = pad(data, AES.block_size)
        ciphertext = cipher.encrypt(padded)

        #Saving Encrypted text to a file
        with open(output, "wb") as file:
            file.write(salt + iv + ciphertext)

        print(f"Encrypted in file: {output}")
    #try-except responsible for error detection
    except FileNotFoundError:
        print(f"File {input} couldn't be found.")
    except Exception as e:
        print(f"Problem encountered during encryption: {e}")

#Function responsible for file decryption
def decrypt(password: str, input: str, output: str):
    try:
        #Reading Encrypted file and separating salt/IV from encrypted text
        with open(input, "rb") as file:
            salt = file.read(16)
            iv = file.read(16)
            ciphertext = file.read()

        #Making a key from password and salt contained in file
        key = derive_key(password, salt)

        #Decryption
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(ciphertext)
        plaintext = unpad(decrypted, AES.block_size)

        #Saving decrypted text to file
        with open(output, "wb") as file:
            file.write(plaintext)

        print(f"Decrypted in file: {output}")
    #try-except responsible for error detection
    except FileNotFoundError:
        print(f"File {input} couldn't be found.")
    except ValueError:
        print(f"Wrong password or corrupted file. - File couldn't be decrypted.")
    except Exception as e:
        print(f"Problem encountered during decryption: {e}")

#Main loop
if __name__ == "__main__":
    while True:
        #Conditional instruction responsible for using option chosen by user
        choice = input("\nDo you want to encrypt, decrypt or exit? (e/d/x): ")
        if choice == "e":
            password = input("Input password: ")
            input_file = input("Name of input file: ")
            output_file = input("Name of output file: ")
            try:
                encrypt(password, input_file, output_file)
            except Exception as e:
                print(f"Problem encountered: {e}")
        elif choice == "d":
            password = input("Input password: ")
            input_file = input("Name of input file: ")
            output_file = input("Name of output file: ")
            try:
                decrypt(password, input_file, output_file)
            except Exception as e:
                print(f"Problem encountered: {e}")
        elif choice == "x":
            break
        else:
            print("Invalid choice")