import socket
import json
from random import randint

# message format
VERSION_BUFF_SIZE = 1
VERSION = 2
HEADER = 64
FORMAT = 'utf-8'

# network
SERVER = socket.gethostname()
SERVER_IP = socket.gethostbyname(SERVER)
PORT = 8080
ADDR = (SERVER_IP, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = str(len(message)).encode(FORMAT)
    msg_length += b' ' * (HEADER - len(msg_length))

    # Convert version to a string and ensure it's 1 byte in length
    msg_version = str(VERSION).encode(FORMAT)[:VERSION_BUFF_SIZE]

    # Send the version, header, and the actual message
    client.send(msg_version)
    client.send(msg_length)
    client.send(message)


def crypt(msg, key):
    crypt_msg = ''
    for c in msg:
        crypt_msg += chr(ord(c) ^ key)
    return crypt_msg


g = randint(1, 100)
n = randint(1, 100)
client_private_number = randint(1, 100)
client_param = (g ** client_private_number) % n

client_name = input("Enter your name: ")

# Diffie-Hellman handshake
# serialize the g, n and client parameter
json_string = json.dumps([str(g), str(n), str(client_param)])
send(json_string)
print(f"Sent client parameter {client_param} to server")
from_server = client.recv(2048).decode(FORMAT)
server_param = json.loads(from_server)
if isinstance(server_param, dict) and server_param.get('status') == 'error':
    raise ValueError(server_param)

print(f"Got server_param {server_param}")
client_key = (server_param ** client_private_number) % n
print(f"Found key {client_key}")

try:
    while True:
        value = input("Please enter a string to send: ")
        send(json.dumps({
            "name": client_name,
            "data": crypt(value, client_key)
        }))
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting...")
finally:
    client.close()
