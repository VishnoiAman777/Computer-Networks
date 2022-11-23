import socket
import sys
import struct
import os

# Initialise socket stuff
TCP_IP = "127.0.0.1" # Only a local server
TCP_PORT = 60000 # Just a random choice
BUFFER_SIZE = 1024 # Standard chioce
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect_flag = 0

def connect_server():
    global connect_flag
    try:
        s.connect((TCP_IP, TCP_PORT))
        print( "Connection sucessful")
        connect_flag = 1
    except:
        print ("Unable to connect to server")

def list_files():
    if connect_flag == 0:
        print("\n\nConnect to server first")
        return
    else:
        s.send(str.encode("LIST"))
        # Wait for server go-ahead
        all_files = []
        data = s.recv(BUFFER_SIZE)
        while data != b'-':
            all_files.append(data.decode())            
            s.send(str.encode("File rcvd"))
            data = s.recv(BUFFER_SIZE)
        s.send(str.encode("Done"))
        print("All files in the folder are \n", ','.join(all_files))
    return

def delf(file_name):
    if connect_flag == 0:
        print("Connection not established")
        return
    s.send(str.encode("DELF"))
    s.recv(BUFFER_SIZE)
    s.send(str.encode(file_name))
    try:
        file_exists = struct.unpack("i", s.recv(4))[0]
        if file_exists == -1:
            print ("The file does not exist on server")
            return
    except:
        print ("Couldn't determine file existance")
        return
    
    confirm_delete = input("Are you sure you want to delete {}? (Y/N)\n".format(file_name)).upper()
    while confirm_delete != "Y" and confirm_delete != "N" and confirm_delete != "YES" and confirm_delete != "NO":
        # If user input is invalid
        print ("Command not recognised, try again")
        confirm_delete = input("Are you sure you want to delete {}? (Y/N)\n".format(file_name)).upper()

    if confirm_delete == "Y" or confirm_delete == "YES":
        # User wants to delete file
        s.send(str.encode("Y"))
        # Wait for conformation file has been deleted
        delete_status = s.recv(BUFFER_SIZE).decode()
        if delete_status == "1":
            print ("File successfully deleted")
            return
        else:
            # Client will probably send -1 to get here, but an else is used as more of a catch-all
            print ("File failed to delete")
            return
    else:
        s.send("N")
        print ("Delete cancelled by user!")
        return
    
def dwld(file_name):
    if connect_flag == 0:
        print("Connection not established")
        return
    s.send(str.encode("DWLD"))
    s.recv(BUFFER_SIZE)
    s.send(str.encode(file_name))
    # Get file size (if exists)
    file_size = s.recv(BUFFER_SIZE).decode()
    print("File Size", file_size)
    if file_size == "-1":
        print ("File does not exist on the server")
        return
    file_size = int(file_size)
    # It's a signal to send the file
    s.send(str.encode("1"))
    # Enter loop to recieve file
    output_file = open(file_name.split("/")[-1], "wb")
    bytes_recieved = 0
    print ("\nDownloading the file")
    while bytes_recieved < file_size:
        # Again, file broken into chunks defined by the BUFFER_SIZE variable
        l = s.recv(BUFFER_SIZE)
        output_file.write(l)
        bytes_recieved += BUFFER_SIZE
    output_file.close()
    print ("Successfully downloaded {}".format(file_name))
    # Tell the server that the client is ready to recieve the download performance details
    s.send(str.encode("1"))
    # Get performance details
    time_elapsed = s.recv(BUFFER_SIZE).decode()
    print ("Time elapsed: {}s\nFile size: {}b".format(time_elapsed, file_size))
    return

def upld(file_name):
    if connect_flag == 0:
        print("You should connect to server first")
        return
    # Upload a file
    print ("\nUploading file: {}...".format(file_name))
    try:
        content = open(file_name, "rb")
    except FileNotFoundError:
        print("File not found on the client side")
        return
    s.send(str.encode("UPLD"))
    # Wait for server ok
    s.recv(BUFFER_SIZE)
    # Send file name size and file name
    s.send(str.encode(file_name))
    # Wait for server ok then send file size
    s.recv(BUFFER_SIZE)
    f_size= os.path.getsize(file_name)
    print("File_Size",f_size)
    s.send(str.encode(str(f_size)))
    s.recv(BUFFER_SIZE)
    # Send the file in chunks defined by BUFFER_SIZE
    # Doing it this way allows for unlimited potential file sizes to be sent
    l = content.read(BUFFER_SIZE)
    print ("\nSending...")
    while l:
        s.send(l)
        l = content.read(BUFFER_SIZE)
    content.close()
    # Get upload performance details
    upload_time = s.recv(BUFFER_SIZE).decode()
    upload_size = s.recv(BUFFER_SIZE).decode()
    print (file_name, "successfully sent.", "Size:", upload_size, "time taken", upload_time)
    return



def quit():
    if connect_flag == 1:
        s.send(str.encode("QUIT"))
        # Wait for server go-ahead
        data = s.recv(BUFFER_SIZE)
        print(data)
        s.close()
        print ("Server connection ended")
    else:
        print("You should connect first")
    return

while True:
    # Listen for a command to be performed
    print ("\n\nWelcome to the FTP client.\n\nCall one of the following functions:\nCONN           : Connect to server\nUPLD file_path : Upload file\nLIST           : List files\nDWLD file_path : Download file\nDELF file_path : Delete file\nQUIT           : Exit")
    prompt = input("Enter what you want to do: ")
    if prompt[:4].upper() == "CONN":
        connect_server()
    elif prompt[:4].upper() == "UPLD":
        upld(prompt[5:])
    elif prompt[:4].upper() == "LIST":
        list_files()
    elif prompt[:4].upper() == "DWLD":
        dwld(prompt[5:])
    elif prompt[:4].upper() == "DELF":
        delf(prompt[5:])
    elif prompt[:4].upper() == "QUIT":
        quit()
        break
    else:
        print ("Command not recognised; please try again")