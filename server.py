import socket
from http_handler import *
import time
from uuid import uuid1
from pprint import pprint
import sys

cookies = {}
          
METHOD  =      {
                 'GET'           : get_handler,
	         'POST'          : post_handler,
                 'DELETE'        : delete_handler,
                 'HEAD'          : head_handler,
                 'FILE'          : file_handler,
               }

def add_route(method,path,func):
    routes[method][path] = func


'''
*********************************************************************
Server Functions
'''

def start_server(hostname, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((hostname, port))
        print "server started at port:", port
        sock.listen(3)
        while True:
            client_socket, message = accept_connection(sock)
            if message:
                request_handler(client_socket,message)
            else:
                client_socket.close()
    except KeyboardInterrupt:
        print "Bye Bye"
    finally:
        sock.close()


def accept_connection(sock):
    data = ""
    (client_socket,(ip,port)) = sock.accept()
    print "connection request from client:", ip
    while True:
        buff = client_socket.recv(2048)
        if not buff:
            break
        data += buff
        if '\r\n\r\n' in data and 'Content-Length' in data:
            header, body   = buff.split('\r\n\r\n')
            line = [i.strip() for i in header.split('\n') if 'Content-Length' in i]
            content_length = int(line[0].split(':')[1].strip())
            if len(body) == content_length:
                break
        if '\r\n\r\n' == data[-4:]:
            break
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
    header = header.strip().split('\r\n')
    first = header.pop(0)
    request["method"]   = first.split()[0]
    request["path"]     = first.split()[1]
    request["protocol"] = first.split()[2]
    if header:
        request['header']   = header_parser(header)
    else:
        request['header']    = {'Cookie':""}
    request['body']     = body
    return request


def header_parser(message):
    header={}
    for each_line in message:
        key, value  = each_line.split(": ",1)
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
    cookie_handler(request, response)
    method_handler(request,response)
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
    
def response_handler(request, response):
    response['Date']       = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    response['Connection'] = 'close'
    response['Server']     = 'geekskool_magic_server'
    response_string        = response_stringify(response)
    request['socket'].send(response_string)
    request['socket'].close()
    

