# client.py
import socket                   # Import socket module
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket object
host = socket.gethostname()     # Get local machine name or we can even do 127.0.0.1
port = 60000                  # Reserve a port for your service.

s.connect((host, port))  # Connecting to the server
ind = 1

file_name = input("Please enter the file Name: ")
s.send(str.encode(file_name))
data = s.recv(1024).decode()

if data == "404: File-not-Found":
    print(data)
    exit()
print("Successfully found file", data)

s.send(str.encode(f"Word_#{ind}")) # Sending the initial message
with open('received_file.txt', 'wb') as f:
    while True:
        data = s.recv(1024) # Here 1024 is the size of buffer
        print('data=%s', (data))
        f.write(data + b' ')
        if data == b'404: File-not-Found':
            break
        if data == b'EOF':
            print('Successfully get the file')
            break

        # write data to a file
        
        ind += 1
        s.send(str.encode(f'Word_#{ind}'))
        

s.close() # Closing the connection