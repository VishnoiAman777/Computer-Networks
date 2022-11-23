import socket
from socket import timeout
import datetime
import argparse
import time
import matplotlib.pyplot as plt
serverAddressPort   = ("127.0.0.1", 20001)

parser = argparse.ArgumentParser(prog = 'UDPEcho',description = 'Used to get echo packets back')
# parser.add_argument('--time_interval', type=int, default=1)           # positional argument
# parser.add_argument('--num_packets', type=int, default=15)      # option that takes a value
parser.add_argument('--packet_size', type=int, default=10)
args = parser.parse_args()

f = open('sample_data.txt', 'rb')
data = f.read(args.packet_size)
bufferSize = len(str.encode(str(datetime.datetime.now()))) + args.packet_size 
f.close()

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.settimeout(0.1)

# Send to server using created UDP socket

packets_lost = 0
rtt_lst = []
throughput = []
ind = 0
time_packet =[]
for i in range(20):
    print("Time t=", i, "sec")
    start_time = datetime.datetime.now()
    diff_interval = (datetime.datetime.now() - start_time)
    diff_interval_sec = (diff_interval.seconds) +(diff_interval.microseconds * (10**(-6)))
    pckt_rcvd = 0
    while diff_interval_sec < 1:
        pckt_rcvd += 1
        curr_time = datetime.datetime.now()
        # print("PacketSent")
        UDPClientSocket.sendto(str.encode(str(curr_time) + " " + data.decode()), serverAddressPort)
        # Capturing packets only for 1 sec
        diff_interval = (datetime.datetime.now() - start_time)
        diff_interval_sec = (diff_interval.seconds) +(diff_interval.microseconds * (10**(-6)))
        try:
            msgFromServer = UDPClientSocket.recvfrom(bufferSize)[0]

        except timeout:
            # print('Packet lost.')
            packets_lost += 1
            continue
        # msg = "Message from Server {}".format(msgFromServer[0])
        curr_time = datetime.datetime.now()
        rtt =  (curr_time- datetime.datetime.strptime(' '.join(msgFromServer.decode().split()[:2]), '%Y-%m-%d %H:%M:%S.%f'))
        # print()  
        rtt_lst.append((rtt.seconds) +(rtt.microseconds * (10**(-6))))
        tmp = datetime.datetime.now()
        time_packet.append(tmp)

    throughput.append(pckt_rcvd * args.packet_size)    

# print("Percentage of Packets Lost", str((packets_lost/args.num_packets)*100 )+ "%")
# print("Throughput", throughput)
# print("rtt", rtt_lst)



plt.plot(throughput, 'bo', lw = 2, linestyle = 'dashed')
plt.ylim(0, 5000)
plt.ylabel("Average Througput")
plt.xlabel("Time")
plt.title("Average Throughput(bytes received per sec)")
plt.show()

# print(rtt_lst, time_packet)
plt.plot(time_packet,rtt_lst, lw = 2, linestyle = 'solid')
plt.ylim(0, 0.001)
# plt.xlim(0, 1)
plt.ylabel("Average Delay")
plt.xlabel("Time")
plt.title("Average Delay")
plt.show()


