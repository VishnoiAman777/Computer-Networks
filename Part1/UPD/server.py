import socket                   # Import socket module
import os
port = 60000                    # Reserve a port for your service.
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket object
s.bind(('127.0.0.1', port))            # Bind to the port
print('Server listening....')

file_path = "/home/aman/Desktop/Computer Networks/Part1/File/file.txt"
file_exists = os.path.exists(file_path)
file_tokens = None
if file_exists:
   f = open(file_path,'r')
   file_tokens = f.read().split()

# It is able to cater one connection at a time
# conn, addr = s.accept()     # Establish connection with client.
while True:
   data, address = s.recvfrom(1024)     # 1024: Size of buffer on the server side
   data = data.decode('ascii') 
   print('Server received', repr(data))
   if not file_exists:
      s.sendto(str.encode("404: File-not-Found"), address)
   else:
      index = data.split("#")[-1]
      s.sendto(str.encode(file_tokens[int(index)-1]), address)

      print(f'Done sending Word_#{index}' )
      if file_tokens[int(index)-1] == 'EOF':
         print("Server listening..........")

