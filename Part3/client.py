import socket
import argparse
import datetime

# Command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-port", dest= "port_num", help="Port number", type=int, default=4000)
parser.add_argument("-ip", dest="ip_address", help="IP Address of Server")
parser.add_argument("-n", dest="messages", type=int, default=5)
args = parser.parse_args()

# Taking the server IP and Port
serverIP = args.ip_address
port = int(args.port_num)
total_messages = int(args.messages)
BUFFER_SIZE = 1024

# Getting information about the server using addrinfo()
addr_info = socket.getaddrinfo(serverIP, port)

# Extracting serverIP and Port from addr_info
serverIP = addr_info[0][4][0]
port = int(addr_info[0][4][1])

# Checking the Address Family from the addr_info to create socket
f = addr_info[0][0]

# Create a TCP socket
s = socket.socket(family=f, type=socket.SOCK_STREAM)

# Connecting to the server
s.connect((serverIP, int(port)))

print(f'Sending {total_messages} packets to the server:\n')
i = 0

# sending n packets
while total_messages:

    total_messages -= 1
    i += 1

    # sending packet to server and getting sending time
    print(f'Sending Packet({i})...')
    send_time = datetime.datetime.now().timestamp()
    s.sendall('ping'.encode())

    # recieving ack from server and getting receiving time
    ack = s.recv(BUFFER_SIZE)
    receive_time = datetime.datetime.now().timestamp()

    # Printing necessary info in terminal including RTT
    print(f'Packet({i}) sent successfully')
    print(f"Server's response: {ack.decode()}")

    print(f"[+] RTT: {receive_time-send_time}")

    print('*'*25)
    print()

print(f'{i} packets sent.')
print(f'Closing connection...')

# Tell the server to stop
s.sendall("!close".encode())

# Close the socket
s.close()
print('Connection closed')