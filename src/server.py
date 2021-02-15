import socket
import threading
#ustawienenia naszego gniazda, port oraz nagłówek domyslny
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8' #formatowanie tekstu
DISCONNECT_MESSAGE = "!DISCONNECT"#formatowanie tekstu

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #tworzenie gniazda
server.bind(ADDR) #przypisanie adresu

dictionary = {} #deklaracja slownika do odebrnia

def handle_message_dict( message ) : #funkcja odbierająca i interpretujaca slownik
    i = 1
    dict = {}
    while i < len(message)- 1 : #podzial slownika na bity, odczytanie znaków
        dict[ message[i] ] = ''
        j = i
        i = i+2
        while message[i] is not ',' :
            dict[ message[j] ] = dict[ message[j] ] + message[i] #przepisywanie odczytanych znakow do slownika
            i = i + 1
        i = i + 1
    print('Otrzymany slownik: ' , dict) #wyswietlenie zawartosci
    return dict

def translate(message,dict) : #funkjca tlumaczaca odebrane dane wg slownika
    solution = ''
    str = ''
    for char in message :
        str = str + char
        for element in dict :
            if dict[element] == str : #porownainie bitowej postaci znaku do znakow ze slownika
                solution = solution + element
                str = ''
    print ( 'Przetlumaczone ' + solution ) #wyswietlanie zawartosci


def handle_client(conn, addr): #funkcja obslugujaca polaczenie gniazda
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True #deklaracja otwartego polaczenia
    while connected: #nastawienei na odbior podczas pracy programu
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE: #zamkniecie polaczenia po otrzymaniu wiadomosci
                connected = False

            #print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT)) #potwierdzenie odbioru wiadomosci


            if(msg[0] == '/') : #odbieranie slownika
                dictionary = handle_message_dict(msg)
            else: #odbieranie wiadomosci i jej tlumaczenie
                translate(msg,dictionary)

    conn.close() #zamkniecie polaczenia


def start():
    server.listen() #start nasluchiwania
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr)) #rozpoczecie watku polaczenia
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}") #wyswietlanie aktywnych polaczen


print("[STARTING] server is starting...")
start() #wywolanie funkcji staru porgramu odbierajacego dane