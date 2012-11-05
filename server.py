import socket
import sys
import re

#http://stackoverflow.com/questions/4685217/parse-raw-http-headers
#credit: Brandon Rhodes
from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO

class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = StringIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message
#end credit to stackoverflow

#paths
htdocPath = "htdocs"
errPath = "HTTPerr/"

host = ''
port = 80
size = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#load our error response
errF = open(errPath + "404.html", 'r')
err = errF.read()
errF.close() 

s.bind((host, port))
backlog = 128
s.listen(backlog)
while 1:
    client, address = s.accept()
    data = client.recv(size)
    if data:
        data = data.decode("ascii") #convert response from byte array to string
		
		#use our stack overflow stuff so we can parse our request easier
        request = HTTPRequest(data)
        print(request.path) 
		#how easy was that?
		
        try:
			#open the file and send it off to the client, remember our client and file handlers need to be closed
            f = open(htdocPath + request.path, 'r')
            resp = f.read()
            f.close()
            client.send(resp)
            client.close()
        except:
			#lets just assume a 404 for laziness sake, it makes no difference to the client what error they got
			#they just know they can't view the web page (REMEMBER CLIENT HANDLER)
            client.send(err)
            client.close()