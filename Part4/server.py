import socket
import datetime
from socket import timeout
import os
import struct
TCP_IP = "127.0.0.1"
TCP_PORT = 60000 
BUFFER_SIZE = 1024 
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# s.settimeout(2)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn, addr = None, None

print("Server ready to accept connections")
conn, addr = s.accept()
print("Connection Esatblished Successfully by", addr)

def list_files():
    all_files = os.listdir("Files")
    i = 0
    while i != len(all_files):
        conn.send(str.encode(all_files[i]))
        try:
            conn.recv(BUFFER_SIZE)
        except timeout:
            continue
        i += 1
    conn.send(str.encode("-"))
    conn.recv(BUFFER_SIZE)
    print("All file names successfully sent")

def delf():
    # Send go-ahead
    conn.send(str.encode("1"))
    # Get file details
    # file_name_length = struct.unpack("h", conn.recv(2))[0]
    file_name = conn.recv(BUFFER_SIZE).decode()
    # Check file exists
    if os.path.isfile(file_name):
        conn.send(struct.pack("i", 1))
    else:
        # Then the file doesn't exist
        conn.send(struct.pack("i", -1))
    # Wait for deletion conformation
    confirm_delete = conn.recv(BUFFER_SIZE).decode()
    if confirm_delete == "Y":
        try:
            # Delete file
            os.remove(file_name)
            conn.send(str.encode("1"))
        except:
            # Unable to delete file
            print ("Failed to delete {}".format(file_name))
            conn.send(struct.pack("i", -1))
    else:
        # User abandoned deletion
        # The server probably recieved "N", but else used as a safety catch-all
        print ("Delete cancelled by client!")
        return

def dwld():
    conn.send(str.encode("1"))
    file_name = conn.recv(BUFFER_SIZE).decode()
    print("filename passed", file_name)
    if os.path.isfile(file_name):
        # Then the file exists, and send file size
        print("File Exists on the server")
        conn.send(str.encode(str(os.path.getsize(file_name))))
    else:
        print ("File Doesn't exists on the server")
        conn.send(str.encode("-1"))
        return
    conn.recv(BUFFER_SIZE)
    # Enter loop to send file
    start_time = datetime.datetime.now()
    content = open(file_name, "rb")
    l = content.read(BUFFER_SIZE)
    while l:
        conn.send(l)
        l = content.read(BUFFER_SIZE)
    content.close()

    # It's a signal that everything went well and the client is ready to get performance
    conn.recv(BUFFER_SIZE)
    # This is the time taken by the network to send the file completely
    conn.send(str.encode(str((datetime.datetime.now() - start_time).total_seconds())))
    return

def upld():
    conn.send(str.encode("1"))
    file_name = conn.recv(BUFFER_SIZE).decode()
    # Send message once server is ready to recieve file details
    conn.send(str.encode("1"))
    # Recieve file name length, then file name
    file_size = int(conn.recv(BUFFER_SIZE).decode())
    # Now we have the file length and the file name, let's now send an ack to client
    # so that he can start sending the files
    conn.send(str.encode("1"))
    print(file_name, file_size)
    # Recieve file size
    # file_size = int(conn.recv(BUFFER_SIZE).decode())
    # Initialise and enter loop to recive file content
    start_time = datetime.datetime.now()
    output_file = open(f"Files/{file_name}", "wb")
    # This keeps track of how many bytes we have recieved, so we know when to stop the loop
    bytes_recieved = 0
    print ("\nRecieving file data")
    while bytes_recieved < file_size:
        l = conn.recv(BUFFER_SIZE)
        output_file.write(l)
        bytes_recieved += BUFFER_SIZE
    output_file.close()
    print( "\nRecieved file: {}".format(file_name))
    # Send upload performance details
    conn.send(str.encode(str((datetime.datetime.now() - start_time).total_seconds())))
    conn.send(str.encode(str(file_size)))
    return


def quit_connection():
    global conn, addr
    print("Connection over by the client", addr)
    print("Closing Connection")
    conn.send(str.encode("Connection Over"))
    conn.close()
    print("Server Listening")
    conn, addr = s.accept()
    print("Connection Esatblished Successfully by", addr)

while True:
    # Enter into a while loop to recieve commands from client
    print ("\n\nWaiting for instruction")
    data = conn.recv(BUFFER_SIZE)
    data = data.decode()
    print("Instructions From Client", data)
    # Check the command and respond correctly
    if data == "QUIT":
        quit_connection()
    elif data == "LIST":
        list_files()
    elif data == "DWLD":
        dwld()
    elif data == "DELF":
        delf()
    elif data == "UPLD":
        upld()
    data = None

