g = 10
n = 7
client_private_number = 2
server_private_number = 3

client_param = (g ** client_private_number) % n
server_key = (client_param ** server_private_number) % n
server_param = (g ** server_private_number) % n
client_key = (server_param ** client_private_number) % n

print(client_param)
print(server_param)
print(server_key)
print(client_key)
