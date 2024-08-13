# Poor's man PoC for TLS handshake

### Description

The goal of TLS is to have the CLIENT(s) and the SERVER agree on the same key. The key will be used to encrypt the traffic between them. Multiple clients are supported.

```
1. CLIENT starts the handshake by generating 3 numbers, g and n which are public and x which is private
2. CLIENT sends g, n and parameter g raised to the power x modulo n to the SERVER
3. SERVER receives the data from the CLIENT, generates a private number y and then raises the CLIENT’s parameter to the power of y and does a modulo of n and with basic math this is equal to g to the power x multiplied by y module n. This now becomes the KEY. 
4. SERVER sends its data with g raised to the power of y modulo n
5. CLIENT raises server parameter to the power of x which equates to g to the power x multiplied by y module n.
```

Both the client and server have the same KEY. This KEY exchange algorithm is called Diffie–Hellman key exchange.

### Code
[**client.py**](client.py) - talks to the server and tries the TLS handshake\
[**main.py**](main.py) - contains the actual math demo\
[**server.py**](server.py) - listen on 8080 for a client

### Usage
Start the server:
```
terminal_1 > python ./server.py
```
Start one client:
```
terminal_2 > python ./client.py
```
Start another client:
```
terminal_3 > python ./client.py
```

### Reference

https://www.youtube.com/watch?v=64geP_LAZ5U

https://www.youtube.com/watch?v=3QiPPX-KeSc

https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange#Cryptographic_explanation

