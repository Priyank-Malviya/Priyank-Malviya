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
    print(message)
    client.send(message)


def handle_connection(client):
    stop = False
    while not stop:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            nickname = None
            addr = None
            for key, value in clients.items():
                if value == client:
                    addr = key
                    break
            for key, value in nicknames.items():
                if value == addr:
                    nickname = key
                    break
            if nickname and addr:
                del nicknames[nickname]
                del clients[addr]
        
            stop = True


def main():
    print('Server is running...')

    while True:

        client, addr = server.accept()

        print(f"Connected to {addr}")

        nickname = client.recv(1024).decode('utf-8')
        if nickname not in nicknames:
            res = "1"
            nicknames[nickname] = addr
            clients[addr] = client
            print(f"Nickname is {nickname}")
            client.send(f"{res}".encode('utf-8'))

            nicknames_json = json.dumps(nicknames)
            send_message(client, nicknames_json.encode('utf-8'))

            thread = threading.Thread(target=handle_connection, args=(client,))
            thread.start()
        else:
            res = "0"
            client.send(f"{res}".encode('utf-8'))
            client.close()


if __name__ == '__main__':
    main()
