#!/usr/bin/env python
 
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import os
import RPi.GPIO as GPIO
import time

L1ON = 21
L2ON = 20
L3ON = 16

L1OFF = 26
L2OFF = 19
L3OFF = 13

def Pulse(light):
    GPIO.output(light,True)
    time.sleep(1)
    GPIO.output(light,False)
    
def Pulse3(l1,l2,l3):
    GPIO.output(l1,True)
    time.sleep(.5)
    GPIO.output(l1,False)
    GPIO.output(l2,True)    
    time.sleep(.5)
    GPIO.output(l2,False)
    GPIO.output(l3,True)    
    time.sleep(.5)
    GPIO.output(l3,False)

def SetLight(strName, state):
    if strName == 'UNO':
        if state == 'ON':
            Pulse(L1ON)
        elif state == 'OFF':
            Pulse(L1OFF)
    elif strName == 'DOS':
        if state == 'ON':
            Pulse(L2ON)
        elif state == 'OFF':
            Pulse(L2OFF)
    elif strName == 'TRES':
        if state == 'ON':
            Pulse(L3ON)
        elif state == 'OFF':
            Pulse(L3OFF)
    elif strName == 'WEMO1':
        if state == 'ON':
            print(os.popen('curl -X POST https://maker.ifttt.com/trigger/wemo1_on/with/key/YOURKEY'))
        elif state  == 'OFF':
            print(os.popen('curl -X POST https://maker.ifttt.com/trigger/wemo1_off/with/key/YOURKEY'))
    elif strName == 'ALL':
        if state == 'ON':
            Pulse3(L1ON,L2ON,L3ON)
            print(os.popen('curl -X POST https://maker.ifttt.com/trigger/wemo1_on/with/key/YOURKEY'))
        elif state == 'OFF':
            Pulse3(L1OFF,L2OFF,L3OFF)
            print(os.popen('curl -X POST https://maker.ifttt.com/trigger/wemo1_off/with/key/YOURKEY'))


ALLLIGHTS = [L1ON,L1OFF,L2ON,L2OFF,L3ON,L3OFF]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Initialize all of the light ports
for l in ALLLIGHTS:
    GPIO.setup(l, GPIO.OUT)
    GPIO.output(l,False)




 
# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
 
  # GET
  def do_GET(self):
        # Send response status code
        self.send_response(200)
        print("GET")
        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()
 
        # Write content as utf-8 data
        self.wfile.write(bytes(index, "utf8"))
        return
  def do_POST(self):
        # Send response status code
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(bytes(index, "utf8"))
        # Send headers
        
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        if ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
            strname = postvars.get(b"lightname",b"dne")
            state = postvars.get(b"state",b"dne")
            if strname != b"dne":
                SetLight((b''.join(strname)).decode("utf-8"),(b''.join(state)).decode("utf-8"))                                      
            print(strname)
            print(state)
 

print('starting server...')

file = open("/home/pi/CodeProjs/indexlocal.html","r")
index = file.read()


# Server settings
server_address = ('', 7072)
httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
print('running server...')
httpd.serve_forever()
 
 
