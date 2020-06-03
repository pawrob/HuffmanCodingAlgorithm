import socket
from Node import Node
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "10.9.25.109"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

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


string = 'ZAWSZE I WSZEDZIE POLICJA JEBANA BEDZIE!'

class NodeTree(object):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right
    def children(self):
        return (self.left, self.right)
    def nodes(self):
        return (self.left, self.right)
    def __str__(self):
        return '%s_%s' % (self.left, self.right)

def huffmanCodeTree(node, left=True, binString=''):
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffmanCodeTree(l, True, binString + '0'))
    d.update(huffmanCodeTree(r, False, binString + '1'))
    return d

freq = {}
for c in string:
    if c in freq:
        freq[c] += 1
    else:
        freq[c] = 1

freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
nodes = freq

while len(nodes) > 1:
    (key1, c1) = nodes[-1]
    (key2, c2) = nodes[-2]
    nodes = nodes[:-2]
    node = NodeTree(key1, key2)
    nodes.append((node, c1 + c2))
    nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

huffmanCode = huffmanCodeTree(nodes[0][0])
print(' Znak - Kod Huffmana ')

print(huffmanCode)
messageToSend = ''
dictionaryToSend = '/'
for char in string:
    messageToSend = messageToSend + huffmanCode[char]

#Przepisanie slownika na string
for char in huffmanCode :
    dictionaryToSend = dictionaryToSend + char + ':' + huffmanCode[char] + ','

print(dictionaryToSend)
print(messageToSend)
#Trzeba value puscic przez gniazdo wraz z dictionary
#a nastepnie je rozszyfrować po stronie serwera zapewne

send(dictionaryToSend)
send(messageToSend)



send(DISCONNECT_MESSAGE)