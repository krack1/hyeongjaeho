import socket
import time
import json
import httplib
import time



#create a coscket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#get local machine name
host = "192.168.0.6"

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


	decoded = json.loads(data)
	print decoded['hue']
	print decoded['on']
	print decoded['sat']
	print decoded['bri']
	clientsocket.close()

