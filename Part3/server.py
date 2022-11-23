import socket
import argparse

# Command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-port", "--port", help="Port number", type=int, default=4000)
parser.add_argument("-ip", "--ip", help="IP Address of Server")
args = parser.parse_args()

# Taking the server IP and Port
serverIP = args.ip
port = args.port
# Default Values
BUFFER_SIZE = 1024

# Getting information about the server using addrinfo()
addr_info = socket.getaddrinfo(serverIP, int(port))

# Extracting serverIP and Port from addr_info
serverIP = addr_info[0][4][0]
port = int(addr_info[0][4][1])

# Checking the Address Family from the addr_info to create socket
f = addr_info[0][0]

# Create a TCP socket
s = socket.socket(family=f, type=socket.SOCK_STREAM)

# Bind the socket to the address
s.bind((serverIP, port))

# Listen for incoming connections
s.listen(5)
print("Server is listening at the address {}:{}".format(serverIP, port))

while True:
    
    # Accept a connection from the client
    conn, addr = s.accept()
    # Print the connection details
    print('Connection Recieved from Address: ', addr)
    
    with conn:
        
        while True:
            
            # Reciving Data from the client
            data = conn.recv(BUFFER_SIZE)
            print('Recieved Message: ' + data.decode())

            if not data or data == '!close':
                print('Closing Connection')
                break
            
            # Send data to the client
            conn.sendall("ping!".encode())
            print('Acknowledgement sent')
        
    print(f'Connection closed')
    break
