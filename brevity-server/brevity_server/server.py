""" Server for asynchronous chat app """

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from request_builder import RequestBuilder


clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


def accept_incoming_connections():
    """ handling for incoming clients """
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Welcome to the chat", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def update_clients(client):
    users = RequestBuilder()
    users.header('USERS')
    for name in clients.values():
        users.append(str(name))

    packet = bytes(users.req, "utf8")
    try:
        client.send(packet)
    except OSError:
        pass


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Hello %s, welcome.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat." % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        try:
            msg = client.recv(BUFSIZ)
        except ConnectionResetError:
            # all have left
            print("All users have left the chat.")
            break
        try:
            broadcast(msg, name + ": ")
        except OSError:
            # del clients[client]
            # client.close()
            # update_clients(client)
            # update again?
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def check_status():
    for sock in clients:
        try:
            sock.send(bytes('', "utf8"))
        except sock.error:
            clients.pop(sock)
            sock.close()





def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()



