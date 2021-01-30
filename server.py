import socket
import json

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

server_private_number = 3


# handle new connections
def start():
    serv.listen(5)
    while True:
        conn, addr = serv.accept()

        while True:
            print("Client {} connected".format(addr))
            # getting the HEADER first. HEADER contains the message length
            find_msg_length = conn.recv(HEADER).decode(FORMAT)
            if not find_msg_length:
                break
            find_msg_length = int(find_msg_length)
            if find_msg_length == 0:
                break
            data = conn.recv(find_msg_length).decode(FORMAT)
            if not data:
                break
            # hardcoded key length to check if it's matching the server key
            if find_msg_length == 1:
                client_key = json.loads(data)
                if client_key == server_key:
                    print("Keys are the same! TLS works :)")
                break
            json_data = json.loads(data)
            g, n, client_param = [int(e) for e in json_data]
            print("Got client_param {} from client".format(client_param))
            server_key = (client_param ** server_private_number) % n
            print("Found key {}".format(server_key))
            server_param = (g ** server_private_number) % n
            print("Sending server_param {} to client".format(server_param))
            conn.send(json.dumps(server_param).encode(FORMAT))
        conn.close()
        print("Client {} disconnected".format(addr))


print("Starting server on {}".format(ADDR))
start()
