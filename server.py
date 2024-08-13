import socket
import json
from random import randint
from _thread import *

# message format
VERSION_BUFF_SIZE = 1
VERSION = 2
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
    crypt_msg = ''
    for c in msg:
        crypt_msg += chr(ord(c) ^ key)
    return crypt_msg


def start(_conn, _addr):
    try:
        server_key = None
        while True:
            try:
                # Receive the VERSION
                find_version = _conn.recv(VERSION_BUFF_SIZE).decode(FORMAT).strip()
                if not find_version:
                    raise ConnectionResetError(f"Connection lost from {_addr}")

                if find_version != str(VERSION):
                    # Send an error message to the client if invalid version is provided
                    error_response = json.dumps({"status": "error", "message": "Invalid version"})
                    _conn.send(error_response.encode(FORMAT))
                    raise ValueError(f"Received invalid VERSION from {_addr}, terminating connection.")

                # Receive the HEADER (message length)
                find_msg_length = _conn.recv(HEADER).decode(FORMAT).strip()
                if not find_msg_length:
                    raise ConnectionResetError(f"Connection lost from {_addr}")

                find_msg_length = int(find_msg_length)
                if find_msg_length == 0:
                    raise ValueError(f"Received invalid HEADER from {_addr}, terminating connection.")

                # Receive the actual message
                data = _conn.recv(find_msg_length).decode(FORMAT)
                if not data:
                    raise ValueError(f"Received invalid DATA from {_addr}, terminating connection.")

                json_data = json.loads(data)

                if not server_key:
                    # Diffie-Hellman handshake
                    g, n, client_param = [int(e) for e in json_data]
                    print(f"Got client_param {client_param} from client {_addr}")
                    server_key = (client_param ** server_private_number) % n
                    print(f"Found key {server_key}")
                    server_param = (g ** server_private_number) % n
                    print(f"Sending server_param {server_param} to client {_addr}")
                    _conn.send(json.dumps(server_param).encode(FORMAT))
                else:
                    print(f"Encrypted message: {json_data['data']}")
                    print(f"Client {json_data['name']} sent: {crypt(json_data['data'], server_key)}")

            except (socket.error, ConnectionResetError) as e:
                # Handle socket errors and connection resets
                print(f"Socket error or connection reset: {e}")
                break

            except (ValueError, json.JSONDecodeError) as e:
                # Handle specific errors related to data processing
                print(f"Error processing data: {e}")
                break

    except Exception as e:
        # Handle any other unexpected errors
        print(f"Unexpected error: {e}")

    finally:
        _conn.close()
        print(f"Client {_addr} disconnected!")


print(f"Starting server on {ADDR}")
try:
    while True:
        conn, addr = serv.accept()
        print(f"Client {addr} connected.")
        start_new_thread(start, (conn, addr,))
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting...")
