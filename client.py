import socket
from Node import Node
'''HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "10.9.25.109"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR) '''

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

nodes = []
initialNodes = []
def codeMessage(message):
    # ---------SORTOWANKO------------
    dictionary = {}
    for char in message:
        if not char in dictionary :
            dictionary[char] = 1
        else :
            dictionary[char] = dictionary[char] + 1

    sortedDictionary = sorted(dictionary.items(),key=lambda x:x[1])
    print(sortedDictionary)
    # ----------BUCKOWANKO------------
    for char in sortedDictionary :
        initialNodes.append( Node( sortedDictionary[char] ) )

    nodes.append(initialNodes[0])
    for i in range ( 1, len(initialNodes) ) :
        if initialNodes[i].value > nodes[i-1].value :
            nodes.append( Node( nodes[-1].value + initialNodes[i].value, nodes[-2], nodes[-1] ) )






codeMessage("Kurwaa jaaa pierdolee kurwaa heee")


myBytes = bytearray()
myBytes.append(123)
myBytes.append(100)
print(myBytes)
send("Hello World!")
input()
send("Hello Everyone!")
input()
send("Hello Bucki!")

send(DISCONNECT_MESSAGE)