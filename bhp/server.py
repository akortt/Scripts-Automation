import socket
import threading


# Config 
IP = '127.0.0.1'
PORT = 6789

# Server Socket
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP,PORT)) # Bind Expects one Argument, which is a tuple of Host and Port as Address is one single object 
    server.listen()
    print(f'[+] Listening on {IP}:{PORT}')

    while True:
        client, address = server.accept() # We accept the client socket and address
        print(f"[+] Accepted connection from {address}")
        client_handler = threading.Thread(
            target=handle_client, args=(client,)
        ) 
        # Target is callable object which we will invoke a run() to run on a thread
        # We are passing in client --> handle_client(client) 
        # Ensure args is a tuple 

        client_handler.start() # Start Thread Activity 

def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024)
        
        if not data:
            print("[-] Client Disconnected")
            break

        print(f"[+] Received: {data.decode('utf-8')}")
        client_socket.send(b'ACK')

if __name__ == '__main__':
    main()