import socket 
import threading 


host = '127.0.0.1'
port = 5500


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()

clients = [] #anyone connected to the network
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server.accept() # accepts client overtime
        print(f'connected with {str(address)}')

        client.send('nickname'.encode('ascii')) #sends coded message to the client to put his/her nickname
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        #tells everyone the connected clients
        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joinrd the chat y\'all'.encode('ascii'))
        client.send('Connected to server, hurray'.encode('ascii'))

        #thread handling the connection to the client 
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('server is listening')

receive()


