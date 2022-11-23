import socket
import datetime
import time
from random import randint
now = datetime.datetime.now()

localIP     = "127.0.0.1"
localPort   = 20001
f = open('sample_data.txt')
data = f.read()
bufferSize = len(str.encode(str(datetime.datetime.now()) + " " + f"{data}")) 
# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")
 
# Listen for incoming datagrams

while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    # print("Received Message From", bytesAddressPair[1], "message:", bytesAddressPair[0])
    if (randint(1, 100) <= 10):
        continue
    UDPServerSocket.sendto( bytesAddressPair[0], bytesAddressPair[1])
    