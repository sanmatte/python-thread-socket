import socket
import threading
from random import randint

PORT=8010
#IP=socket.gethostbyname(socket.gethostname())
IP="127.0.0.1"
BUFFER  = 1024

FIN=("q", "quit", "fin", "finish", "disconnect")

server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
server.bind((IP,PORT))


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")
    
    while True:
        conn , addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")


def isAlive(msg):
    if msg.lower() in FIN:
        return False


def closeConnection(conn, addr):
    print(f"[FIN] {addr} disconnected")
    conn.close()


def handle_client(conn, addr):

    addr= addr[0]+":"+str(addr[1])
    print(f"[NEW CONNECTION] {addr} connected")

    conn.send(b"200 OK, Do you want to play a game? [Y/yes]")
    msg = conn.recv(BUFFER).decode()

    if not msg.lower()=="y" and not msg.lower()=="yes":
        closeConnection(conn, addr)
        return

    if isAlive(msg):
        closeConnection(conn, addr)
        return
        
    print(f"[{addr}] {msg}")
    conn.send(b"A number from 0 to 9 has just been randomly generated, GUESS IT!")
    play(conn, addr)

    closeConnection(conn, addr)


def play(conn, addr):

    GUESS=randint(0,9)

    counter = 1

    while(True):
        msg=conn.recv(BUFFER).decode()
        print(f"[{addr}] {msg}")

        try:
            message=int(msg)
        except ValueError:
            conn.send("Only numbers are accepted!\n\n[FIN]")
            return
        
        if message==GUESS and counter==1:

                conn.send(b"Yooo, first try. GOOD JOB!\n\n[FIN]")
                return

        elif message==GUESS and counter>1:
            msg="NICE!\ntries: "+str(counter)+"\n\n[FIN]"
            conn.send(msg.encode())
            return
            
        else:

            if message not in range(10):
                conn.send(b"You are not even trying come on \n\n[FIN]")
                return

            conn.send(b"Yeah, YOU WISH SO, try again...")

            counter+=1



print("[STARTING] server is starting...")
start()