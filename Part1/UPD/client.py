# client.py
import socket                   # Import socket module
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket object
port = 60000                  # Reserve a port for your service.

ind = 1
s.sendto(str.encode(f"Word_#{ind}"), ("127.0.0.1", port)) # Sending the initial message


with open('received_file.txt', 'wb') as f:
    while True:
        data = s.recvfrom(1024)[0] # Here 1024 is the size of buffer
        print('data=%s', (data))
        f.write(data + b' ')
        if data == b'EOF':
            print('Successfully get the file')
            break
        # write data to a file
        if data == b'404: File-not-Found':
            print('404: File-not-Found')
            break
        
        ind += 1
        s.sendto(str.encode(f'Word_#{ind}'), ("127.0.0.1", port))
        

s.close() # Closing the connection