import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

dictionary = {}

def handle_message_dict( message ) :
    i = 1
    dict = {}
    while i < len(message)- 1 :
        dict[ message[i] ] = ''
        j = i
        i = i+2
        while message[i] is not ',' :
            dict[ message[j] ] = dict[ message[j] ] + message[i]
            i = i + 1
        i = i + 1
    print('Otrzymany slownik: ' , dict)
    return dict

def translate(message,dict) :
    solution = ''
    str = ''
    for char in message :
        str = str + char
        for element in dict :
            if dict[element] == str :
                solution = solution + element
                str = ''
    print ( 'Przetlumaczone ' + solution )


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            #print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))


            if(msg[0] == '/') :
                dictionary = handle_message_dict(msg)
            else:
                translate(msg,dictionary)

    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()