import socket 

IP = '127.0.0.1'
PORT = 9988

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((IP,PORT))
client.send(b"Hello")
response = client.recv(4096)
print(response.decode())
client.close()