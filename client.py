import socket
import json

# message header
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
    client.send(msg_length)
    client.send(message)


g = 10
n = 7
client_private_number = 2
client_param = (g ** client_private_number) % n

# serialize the g, n and client parameter
json_string = json.dumps([str(g), str(n), str(client_param)])

send(json_string)
print("Sent client parameter {} to server".format(client_param))
from_server = client.recv(2048)
server_param = json.loads(from_server)
print("Got server_param {}".format(server_param))
client_key = (server_param ** client_private_number) % n
print("Found key {}".format(client_key))
send(json.dumps(client_key))
client.close()

