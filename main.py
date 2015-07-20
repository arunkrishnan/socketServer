import socket
from pprint import pprint
import time 

'''
*****************************************************
HTML Response Delivery Functions
'''
def index():
    try:
        with open("./public/index.html","r") as fd:
	    return (fd.read(),'html')
    except IOError:
        return '',''

def login():
    try:
        with open("./login/login.html", "r") as fd:
            return (fd.read(),'html')
    except IOError:
        return '',''

def public(path):
    try:
    	with open('./public' + path,'r') as fd:
    		return (fd.read(), path.split('.')[-1].lower())
    except IOError:
    	return '',''

'''
****************************************************
Server and socket functions
'''
def start_server(hostname, port):
	""" 
	Socket creation
	"""
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((hostname, port))
	print "server started at port:", port
	return sock

def accept_connection(sock):
	(client,(ip,port)) = sock.accept()
	print "connection request from client:", ip
	data = client.recv(1024)
	return client, bytes.decode(data)

'''
*******************************************************
Handler Functions
'''
def request_parser(request):
	parsed_request = {}
        method = request.split("\n")[0]
        print "method"
        print method
	parsed_request["method"] = method.split()[0]
        parsed_request["path"] = method.split()[1]
        parsed_request["protocol"] = method.split()[2]
        header = request.split("\n\n")[0].strip()
        try:
            for each_line in header.split("\n")[1:]:
                key, value = each_line.split(":",1)
                parsed_request[key] = value
        except:
            pass
	return parsed_request

def gen_header(response):
        h = ""
        if (response == 200):
                h = "HTTP/1.1 200 OK\n"
        elif(response == 404):
                h = "HTTP/1.1 404 Not Found\n"
        h +="Date: " + time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        h += "\nConnection: close\n"
        h += "Server: geekskoolblog_server\n"
        return h

def do_GET(request):
        content = ""
	path = request['path']
        print path
        try:
            content, content_type = Routes[path]()
        except KeyError:
            content, content_type = public(path)
 
	if content:
		response = gen_header(200)
	else:
		response = gen_header(404)
		return response
        if content_type == 'html':
            response += "Content-type: text/html\n\n"
        elif content_type == 'css':
            response += "Content-type: text/css\n\n"
        elif content_type == 'jpeg':
            response += "Content-type: image/jpeg\n\n"
        elif content_type == 'jpg':
            response += "Content-type: image/jpg\n\n"
        elif content_type == 'png':
            response += "Content-type: image/png\n\n"
        response += content + "\n\n"

        return response


'''
*******************************************************************************
Hash Tables
'''
Routes = {"/": index,
          "/index": index,
          "/login": login,}

Methods = {
        'GET': do_GET}

'''
********************************************************************************
main
'''

if __name__ == "__main__":
	sock = start_server("127.0.0.1", 8080)
	sock.listen(2)
	while True:
		client, request = accept_connection(sock)
		request = request_parser(request)
                pprint(request)
                response = Methods[request['method']](request)
                print "Sending response"
                client.send(response)
                client.close() 
                
