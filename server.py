import socket
import json
from random import randint

# message header
HEADER = 64
FORMAT = 'utf-8'

# network stuff
HOST = socket.gethostname()
HOST_IP = socket.gethostbyname(HOST)
PORT = 8080
ADDR = (HOST_IP, PORT)

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(ADDR)
serv.listen(5)

server_private_number = randint(1, 100)


def crypt(msg, key):
    print(f"Encrypted message: {msg}")
    crypt_msg = ''
    for c in msg:
        crypt_msg += chr(ord(c) ^ key)
    return crypt_msg


# handle new connections
def start():
    while True:
        conn, addr = serv.accept()
        handshake = False
        print(f"Client {addr} connected.")
        while True:
            # getting the HEADER first. HEADER contains the message length
            find_msg_length = conn.recv(HEADER).decode(FORMAT)
            if not find_msg_length:
                break
            find_msg_length = int(find_msg_length)
            if find_msg_length == 0:
                break
            # getting the actual message, after processing the HEADER
            data = conn.recv(find_msg_length).decode(FORMAT)
            if not data:
                break
            json_data = json.loads(data)
            if not handshake:
                # Diffie-Hellman handshake
                handshake = True
                g, n, client_param = [int(e) for e in json_data]
                print(f"Got client_param {client_param} from client {addr}")
                server_key = (client_param ** server_private_number) % n
                print(f"Found key {server_key}")
                server_param = (g ** server_private_number) % n
                print(f"Sending server_param {server_param} to client {addr}")
                conn.send(json.dumps(server_param).encode(FORMAT))
            else:
                print(f"{json_data['name']} sent: {crypt(json_data['data'], server_key)}")
        conn.close()
        print(f"Client {addr} disconnected!")


print(f"Starting server on {ADDR}")
try:
    start()
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting...")


