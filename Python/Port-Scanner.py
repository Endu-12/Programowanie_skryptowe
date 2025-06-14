import socket

#Function responsible for checking open ports
def scan_ports(host, start_port, end_port):

    #List with open ports
    open_ports = []

    #Checking ports from set range
    for port in range(start_port, end_port + 1):
        #Creating sockets to test port connectivity
        sockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Limiting time for response, preventing blocking operations
        sockets.settimeout(0.5)
        #Testing if the port is open
        result = sockets.connect_ex((host, port))
        if result == 0:
            print(f"port {port}: open")
            open_ports.append(port)
        #Closing the socket
        sockets.close()

    #Printing number of open ports
    if not open_ports:
        print("No open ports")
    else:
        print(f"Number of open port: {len(open_ports)}")
        print(open_ports)

#Using the function
starting_port = int(input("Pick start of the port range: "))
ending_port = int(input("Pick end of the port range: "))
scan_ports("127.0.0.1", starting_port, ending_port)