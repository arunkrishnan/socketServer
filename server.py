import socket
import urlparse
import time
import jsonParser
from uuid import uuid1
import json
from pprint import pprint

cookies = {}
routes =  {
            'get'  : {},
            'post' : {}
          }
          
def add_route(method,path,func):
    routes[method][path] = func


'''
*********************************************************************
Server Functions
'''

def start_server(hostname, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((hostname, port))
    print "server started at port:", port
    try:
        sock.listen(1000)
        while True:
            client_socket, message = accept_connection(sock)
            if message:
                request_handler(client_socket,message)
    except KeyboardInterrupt:
        print "Bye Bye"
        sock.close()


def accept_connection(sock):
    (client_socket,(ip,port)) = sock.accept()
    print "connection request from client:", ip
    data = client_socket.recv(1024)
    return client_socket, data
    

'''
*********************************************************************
Parsers
'''
def request_parser(message):
    request = {}
    try:
        header,body = message.split('\r\n\r\n')
    except IndexError and ValueError:
        header = message.split('\r\n\r\n')[0]
        body = ""
    header = header.split('\r\n')
    first = header.pop(0)
    request["method"]   = first.split()[0]
    request["path"]     = first.split()[1]
    request["protocol"] = first.split()[2]
    request['header']   = header_parser(header)
    request['body']     = body
    return request


def header_parser(message):
    header={}
    for each_line in message:
        key, value = each_line.split(": ",1)
        header[key] = value
    try:
        cookies  = header['Cookie'].split(";")
        client_cookies = {}
        for cookie in cookies:
            head,body = cookie.strip().split('=',1)
            client_cookies[head] = body
        header['Cookie'] = client_cookies
    except KeyError:
        header['Cookie'] = ""
    return header


'''
*********************************************************************
Stringify
'''

def response_stringify(response):
    response_string = response['status'] + '\r\n'
    keys = [key for key in response if key not in ['status','content']]
    for key in keys:
        response_string += key + ': ' + response[key] + '\r\n'
    response_string += '\r\n'
    if 'content' in response:
        response_string += response['content'] + '\r\n\r\n'
    return response_string

'''
*********************************************************************
Handler Functions
'''

def request_handler(client_socket,message):
    response          = {}
    request           = request_parser(message)
    request['socket'] = client_socket
    pprint(request)
    cookie_handler(request, response)
    method_handler(request,response)
    pprint(response)
    response_handler(request, response)
    

def cookie_handler(request, response):
    browser_cookies = request['header']['Cookie']
    if 'sid' in browser_cookies and browser_cookies['sid'] in cookies:
        return
    cookie                 = str(uuid1())
    response['Set-Cookie'] = 'sid=' + cookie
    cookies[cookie]        = {}


def method_handler(request,response):
    handler = METHOD[request['method']]
    handler(request,response)
    

def get_handler(request,response):
    try:
        content, content_type    = routes['get'][request['path']]()
        response['status']       = "HTTP/1.1 200 OK"
        response['content']      = content
        response['Content-type'] = CONTENT_TYPE[content_type]
    except KeyError:
        static_file_handler(request,response)
    

def post_handler(request,response):
    if True:
        content                  = urlparse.parse_qs(request['body'])
        content, content_type    = routes['post'][request['path']](content)
        response['status']       = "HTTP/1.1 200 OK"
        response['content']      = content
        response['Content-type'] = CONTENT_TYPE[content_type]
    '''
    except KeyError:
        print "Landing Not defined"
    '''

def head_handler(request, response):
    pass


def file_handler(request, response):
    pass
	

def delete_handler(request, response):
    pass


def static_file_handler(request, response):
    try:
        with open('./public' + request['path'],'r') as fd:
            response['content']  = fd.read() 
        content_type             = request['path'].split('.')[-1].lower()
        response['Content-type'] = CONTENT_TYPE[content_type]
        response['status']       = "HTTP/1.1 200 OK"
    except IOError:
        err_404_handler(request,response)


def err_404_handler(request, response):
    response['status'] = "HTTP/1.1 404 Not Found"
    

def response_handler(request, response):
    response['Date']       = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    response['Connection'] = 'close'
    response['Server']     = 'geekskool_magic_server'
    response_string        = response_stringify(response)
    request['socket'].send(response_string)
    request['socket'].close()
    


METHOD  =      {
                 'GET'           : get_handler,
	         'POST'          : post_handler,
                 'DELETE'        : delete_handler,
                 'HEAD'          : head_handler,
                 'FILE'          : file_handler,
               }

CONTENT_TYPE = {
                 'html'          : 'text/html',
		 'css'           : 'text/css',
		 'js'            : 'application/javascript',
		 'jpeg'          : 'image/jpeg',
                 'jpg'           : 'image/jpg',
                 'png'           : 'image/png',
		 'gif'           : 'image/gif',
                 'ico'           : 'image/x-icon',
                 'text'          : 'text/plain',
                 'json'          : 'application/json',
	       }


