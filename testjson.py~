import json
import httplib
import time

conn = httplib.HTTPConnection("192.168.0.5")

def on(light):
    conn.request("PUT","/api/newdeveloper/lights/"+str(light)+"/state", '{"on":true}')
    response = conn.getresponse()
    data = response.read()
    if data[3:10] is "success":
        print 'good'
        return True
    else:
        print 'bed'
        return False


def off(ligth):
    conn.request("PUT","/api/newdeveloper/"+str(light)+"/state", '{"on":false}')
    response = conn.getresponse()
    data = response.read()

    if data[3:10] is "success":
        print 'good'
        return True
    else:
        print 'bed'
        return False

on(1)
