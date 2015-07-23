import socket
from pprint import pprint
import time 
import urlparse
import sys
from random import randint
import os

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

def verify_login(usermail, password):
   return 'user'

def login_submit(content):
    try:
       usermail = content['usermail'][0]
       password = content['password'][0]
       user = verify_login(usermail, password)
       if user:
       		return index()
    except:
       pass
    return ' '

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
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((hostname, port))
	print "server started at port:", port
	return sock


def accept_connection(sock):
        print "Accept Connection"
	(client,(ip,port)) = sock.accept()
	print "connection request from client:", ip
	data = client.recv(1024)
	return client, bytes.decode(data)


'''
Parser Functions
'''
def head_parser(message):
    header={}
    try:
        for each_line in message.split("\n")[1:]:
            key, value = each_line.split(":",1)
            header[key] = value
    except ValueError:
        header['content'] = message.rsplit("\n")[-1]
    return header


def request_parser(message):
    request = {}
    first = message.split("\n")[0]
    request["method"]   = first.split()[0]
    request["path"]     = first.split()[1]
    request["protocol"] = first.split()[2]
    request['header'] = head_parser(message.split("\n\n")[0].strip())
    try:
        request['body'] = message.rsplit('\n')[-1]
    except IndexError:
        pass
    return request

def response_stringify(response):
    response_string = response['status'] + '\n'
    keys = [key for key in response if key not in ['status','content']]
    for key in keys:
        response_string += key + ':' + response[key] + '\n'
    response_string += '\n'
    if 'content' in response:
        response_string += response['content'] + '\n\n'
    return response_string


'''
*******************************************************
Handler Functions
'''
def request_handler(message, response):
    request = request_parser(message)
    method_handler(request, response)

def method_handler(request, response):
    handler = METHOD[request['method']]
    handler(request, response)


def get_handler(request, response):
    content = ""
    path = request['path']
    try:
        content, content_type = Routes[path]()
    except KeyError:
        content, content_type = public(path)

    if content:
        gen_header(200)
    else:
        gen_header(404)
        return 
    try:
        response['Content-type'] =  CONTENT_TYPE[content_type]
        response['content'] = content
    except KeyError:
        print "Content Type %r Not defined" %content_type


def post_handler(request, response):
    path = request['path']
    content = urlparse.parse_qs(request['body']) 
    try:
        content, content_type = Landing[path](content)
        if content:
            gen_header(200)
        else:
            gen_header(404)
            return
        try:
            response['Content-type'] = CONTENT_TYPE[content_type]
            response['content'] = content
        except KeyError:
            print "Content Type %r Not defined" %content_type 
    except:
        pass

def head_handler(request, response):
    pass


def file_handler(request, response):
    pass


def delete_handler(request, response):
    pass


def gen_header(response_code):
    if (response_code == 200):
        response['status']= "HTTP/1.1 200 OK"
    elif(response_code == 404):
        response['status'] = "HTTP/1.1 404 Not Found"
    response['Date'] = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    response['Connection'] =  'close'
    response['Server'] = 'geekskoolblog_server'


'''
*******************************************************************************
Hash Tables
'''
Routes = {"/": index,
          "/index": index,
          "/login": login,}

Landing = {"/login_submit" : login_submit,}

METHOD = {'GET'   : get_handler,
	   'POST'  : post_handler,
           'DELETE': delete_handler,
           'HEAD'  : head_handler,
           'FILE'  : file_handler,}

CONTENT_TYPE = {'html': 'text/html',
		'css' : 'text/css',
		'js'  : 'application/javascript',
		'jpeg': 'image/jpeg',
                'jpg' : 'image/jpg',
                'png' : 'image/png',
		'gif' : 'image/gif',
		}

'''
********************************************************************************
main
'''

if __name__ == "__main__":
    try:
        port = 8080
        os.system('fuser -k ' + str(port) + '/tcp')
        sock = start_server("127.0.0.1", port)
        sock.listen(2)
        while True:
            client_socket, message = accept_connection(sock)
            response = {}
	    if message:
	        request_handler(message, response)
                response_string = response_stringify(response)
                client_socket.send(response_string)
            client_socket.close() 
    except KeyboardInterrupt:
        print "Bye"
	sys.exit(0)
            
