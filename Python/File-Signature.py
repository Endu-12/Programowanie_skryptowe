from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

def generate_keys():
    key = RSA.generate(2048)
    private_key = key
    public_key = key.publickey()
    return private_key, public_key

def save_keys(private_key, public_key):
    with open('private_key.pem', 'wb') as file:
        file.write(private_key.exportKey())
    with open('public_key.pem', 'wb') as file:
        file.write(public_key.exportKey())

def sign(path, private_key):
    with open(path, 'rb') as file:
        data = file.read()

    hash = SHA256.new(data)
    signature = pkcs1_15.new(private_key).sign(hash)

    with open(path + ".sig", 'wb') as sig_file:
        sig_file.write(signature)
    print('Signature saved to ' + path + ".sig")

def verify(path, signature_path, public_key):
    with open(path, 'rb') as file:
        data = file.read()
    with open(signature_path, 'rb') as sig_file:
        signature = sig_file.read()

    hash = SHA256.new(data)
    try:
        pkcs1_15.new(public_key).verify(hash, signature)
        print('Signature verified')
    except (ValueError, TypeError):
        print('Signature not verified')

if __name__ == '__main__':
    private_key, public_key = generate_keys()
    save_keys(private_key, public_key)
    while True:
        choice = input('Do you want to sign, verify signature or exit? (s/v/x): ')
        if choice == 's':
            file = input('Enter file path: ')
            try:
                sign(file, private_key)
            except Exception as e:
                print(f"An error occurred: {e}")
        elif choice == 'v':
            file = input('Enter file path: ')
            try:
                verify(file, file + ".sig", public_key)
            except Exception as e:
                print(f"An error occurred: {e}")
        elif choice == 'x':
            break
        else:
            print('Invalid choice')


