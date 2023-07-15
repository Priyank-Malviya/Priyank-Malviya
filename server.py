import socket
import threading
import json

HOST = socket.gethostbyname(socket.gethostname())
PORT = 7292

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

nicknames = {}
clients = {}


def broadcast(message):
        for client in clients.values():
                client.send(message)

def send_message(client, message):
    client.send(message)

def handle_connection(client):
        stop = False
        while not stop:
                try:
                        message= client.recv(1024)
                        broadcast(message)
                except:
                        nickname = None
                        for key, value in nicknames.items():
                                if value == client:
                                        nickname = key
                                        break
                        if nickname:
                                del nicknames[nickname]
                        
                                broadcast(f"{nickname} left the chat!".encode('utf-8'))
                                stop = True

def main():
        print('server is running...')

        while True:
                
                client, addr = server.accept()
                print(f"Connected to {addr}")
                
                nickname = client.recv(1024).decode('utf-8')
                if nickname not in nicknames:
                        res = "1"
                        nicknames[nickname] = addr
                        clients[addr] = client                        
                        print(f"NickName is {nickname}")
                        client.send(f"{res}".encode('utf-8'))
                        

                        thread = threading.Thread(target=handle_connection, args=(client,))
                        thread.start()
                else:
                        client.send("0".encode('utf-8'))

if __name__ == '__main__':
        main() 
