""" Server for asynchronous chat app """

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

MSG_SERVER = socket(AF_INET, SOCK_STREAM)
MSG_SERVER.bind(ADDR)


def accept_incoming_connections():
	""" handling for incoming clients """
	while True:
		client, client_address = MSG_SERVER.accept()
		print("%s:%s has connected." % client_address)
		client.send(bytes("Welcome to the chat", "utf8"))
		addresses[client] = client_address
		Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
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
			# all users have left
			broadcast(bytes("%s has left the chat." % name, "utf8"))
			del clients[client]
			client.close()
			print("%s:%s has disconnected." % addresses[client])
			break

		broadcast(msg, name + ": ")

def broadcast(msg, prefix=""):
	"""Broadcasts a message to all the clients."""

	for sock in clients:
		try:
			sock.send(bytes(prefix, "utf8") + msg)
		except BrokenPipeError:
			return


if __name__ == "__main__":
	MSG_SERVER.listen(5)
	print("Waiting for connection...")
	ACCEPT_THREAD = Thread(target=accept_incoming_connections)
	ACCEPT_THREAD.start()
	ACCEPT_THREAD.join()
	MSG_SERVER.close()
