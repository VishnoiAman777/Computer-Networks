import socket                   # Import socket module
import os
port = 60000                    # Reserve a port for your service.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket object
host = socket.gethostname()     # Get local machine name
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.

print('Server listening....')
conn, addr = None, None

def restart_conn():
   global conn, addr  
   conn, addr = s.accept()     # Establish connection with client.
   f_name = conn.recv(1024).decode()
   return f_name

f_name = restart_conn()
print(os.getcwd())
file_exist = os.path.isfile(f_name)
print("File", f_name, file_exist)
while not file_exist:
   conn.send(str.encode("404: File-not-Found"))
   print("Closing Connection")
   conn.close()
   print("Server listening..........")
   f_name = restart_conn()
   file_exist = os.path.exists(f_name)
# if not os.path.exists(f_name):
#    conn.close()
#    conn, addr = s.accept()
conn.send(str.encode("1"))
file_tokens = None
f = open(f_name,'r')
file_tokens = f.read().split()

# s.send(str.encode("1")) # A confirmation that it is good to go
# It is able to cater one connection at a time
while True:
   data = conn.recv(1024).decode('ascii')      # 1024: Size of buffer on the server side
   print('Server received', repr(data))
   # if not file_exists:
   #    conn.send(str.encode("404: File-not-Found"))
   #    print("Closing Connection")
   #    conn.close()
   #    print("Server listening..........")
   #    conn, addr = s.accept()     # Establish connection with client.

   # else:
   index = data.split("#")[-1]
   conn.send(str.encode(file_tokens[int(index)-1]))
   print(f'Done sending Word_#{index}' )
   if file_tokens[int(index)-1] == 'EOF':
      print("Closing Connection")
      conn.close()
      print("Server listening..........")
      # conn, addr = s.accept()     # Establish connection with client.
      restart_conn()
      f_name = restart_conn()
      print(os.getcwd())
      file_exist = os.path.isfile(f_name)
      print("File", f_name, file_exist)
      while not file_exist:
         conn.send(str.encode("404: File-not-Found"))
         print("Closing Connection")
         conn.close()
         print("Server listening..........")
         f_name = restart_conn()
         file_exist = os.path.exists(f_name)
      # if not os.path.exists(f_name):
      #    conn.close()
      #    conn, addr = s.accept()
      conn.send(str.encode("1"))
      file_tokens = None
      f = open(f_name,'r')
      file_tokens = f.read().split()