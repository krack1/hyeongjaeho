#-*- coding: utf-8 -*-
import socket
import time
import json
import httplib
import time
import sys

def on(light):
	conn.request("PUT","/api/newdeveloper/lights/"+light+"/state",'{"on":true}')
def off(light):
	conn.request("PUT","/api/newdeveloper/lights/"+light+"/state",'{"on":false}')
def putState(light, hue, sat, bri):
	state = {}
	state['hue'] = hue
	state['sat'] = sat
	state['bri'] = bri
	state = json.dumps(state)
	conn.request("PUT","/api/newdeveloper/lights/"+light+"/state", state)


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
		light = decoded['light']
		hue = decoded['hue']
		onled = decoded['on']
		sat = decoded['sat']
		bri = decoded['bri']
		
		print light
		print type(light)
		print onled
		print hue
		print sat
		print bri
					
	
		if onled is True:
			conn = httplib.HTTPConnection("192.168.0.5")
			on(light)
			conn = httplib.HTTPConnection("192.168.0.5")
			putState(light, hue, sat, bri)
		else:

			conn = httplib.HTTPConnection("192.168.0.5")
			off(light)


		clientsocket.close()

serversocket.close()
