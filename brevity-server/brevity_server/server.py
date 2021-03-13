"""Server for multi-threaded (asynchronous) chat application."""

import sys

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from string_builder import StringBuilder


clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Welcome to the chat", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def update_clients(client):
    users = StringBuilder()
    users.header('USERS')
    for name in clients.values():
        users.append(str(name))

    packet = bytes(users.val, "utf8")
    try:
        client.send(packet)
    except OSError:
        print('uh oh')


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat." % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        update_clients(client)
        try:
            msg = client.recv(BUFSIZ)
        except ConnectionResetError:
            # all have left
            print("they're gone")
            break
        try:
            broadcast(msg, name + ": ")
        except OSError:
            client.close()
            del clients[client]
            # update again?
            update_clients(client)
            # at least one is left
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break

# want to update this to display all current client list
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



