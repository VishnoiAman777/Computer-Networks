import socket
from socket import timeout
import datetime
import argparse
import time
serverAddressPort   = ("127.0.0.1", 20001)
f = open('sample_data.txt')
data = f.read()
bufferSize = len(str.encode(str(datetime.datetime.now()) + " " + f"{data}")) 
f.close()

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.settimeout(2)
parser = argparse.ArgumentParser(prog = 'UDPEcho',description = 'Used to get echo packets back')
parser.add_argument('--time_interval', type=int, default=3)           # positional argument
parser.add_argument('--num_packets', type=int, default=10)      # option that takes a value
parser.add_argument('--packet_size', type=int, default=10)
args = parser.parse_args()
# Send to server using created UDP socket

ind = 0
packets_lost = 0
while True:
    ind += 1
    curr_time = datetime.datetime.now()
    print("PacketSent")
    UDPClientSocket.sendto(str.encode(str(curr_time) + " " + data), serverAddressPort)
    try:
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)[0]
    except timeout:
        print('Packet lost.')
        packets_lost += 1
        continue
    send_time = datetime.datetime.strptime(' '.join(msgFromServer.decode().split()[:2]), '%Y-%m-%d %H:%M:%S.%f')
    # msg = "Message from Server {}".format(msgFromServer[0])
    rtt =  (datetime.datetime.now() - send_time)
    print("RTT observed", (rtt.seconds) +(rtt.microseconds * (10**(-6))))
    time.sleep(args.time_interval)
    if ind >= args.num_packets:
        break

print("Percentage of Packets Lost", str((packets_lost/args.num_packets)*100 )+ "%")