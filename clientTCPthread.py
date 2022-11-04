import socket

ADDR=("127.0.0.1",8010)
BUFFER=1024

FIN=("q", "quit", "fin", "finish", "disconnect")

client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
client.connect(ADDR)

while True:
    msg=client.recv(BUFFER).decode()
    print(msg)
    if "FIN" in msg:
        exit()
    msg=input("$: ")
    client.send(msg.encode())
    if msg.lower() in FIN:
        exit()
    

