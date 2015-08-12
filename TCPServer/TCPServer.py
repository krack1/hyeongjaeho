import socket
import time

#create a coscket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#get local machine name
host = "10.255.253.190"

port = 9999

buf = 1024

#bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)

while True:
	#establish a connection
	clientsocket,addr = serversocket.accept()
	data = clientsocket.recv(buf)
	print (data)
	clientsocket.close()

