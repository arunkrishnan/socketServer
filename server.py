import socket
import urlparse
import time

ROUTES =  {
            'get'  : {},
            'post' : {}
          }
          

def start_server(hostname, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((hostname, port))
    print "server started at port:", port
    try:
        sock.listen(1000)
        while True:
            client_socket, message = accept_connection(sock)
            request_handler(client_socket,message)
    except KeyboardInterrupt:
        print "Bye Bye"
        sock.close()


def accept_connection(sock):
    (client_socket,(ip,port)) = sock.accept()
    print "connection request from client:", ip
    data = client_socket.recv(1024)
    return client_socket, bytes.decode(data)
    
	
def static_file_handler(path):
    try:
    	with open('./public' + path,'r') as fd:
    	    return (fd.read(), path.split('.')[-1].lower())
    except IOError:
    	return '',''


def routes(method,path,func):
    ROUTES[method][path] = func


def header_parser(message):
    header={}
    for each_line in message:
        key, value = each_line.split(": ",1)
        header[key] = value
    return header


def request_parser(message):
    request = {}
    header,body = message.split("\r\n\r\n")
    header = header.split('\r\n')
    first = header.pop(0)
    request["method"]   = first.split()[0]
    request["path"]     = first.split()[1]
    request["protocol"] = first.split()[2]
    request['header']   = header_parser(header)
    request['body']     = body
    return request


def response_stringify(response):
    response_string = response['status'] + '\r\n'
    keys = [key for key in response if key not in ['status','content']]
    for key in keys:
        response_string += key + ': ' + response[key] + '\r\n'
    response_string += '\r\n'
    if 'content' in response:
        response_string += response['content'] + '\r\n\r\n'
    return response_string


def request_handler(client_socket,message):
    response = {}
    request  = request_parser(message)
    method_handler(request,response)
    response_handler(client_socket, response)


def response_handler(client_socket, response):
    response_string = response_stringify(response)
    client_socket.send(response_string)
    client_socket.close()


def method_handler(request,response):
    handler = METHOD[request['method']]
    handler(request,response)


def get_handler(request,response):
    try:
        content, content_type = ROUTES['get'][request['path']]()
    except KeyError:
        content, content_type = static_file_handler(request['path'])
    finally:
        generate_response(content, content_type, response)


def post_handler(request,response):
    try:
        content =  urlparse.parse_qs(request['body']) 
        content, content_type = ROUTES['post'][request['path']](content)
    except KeyError:
        print "Landing Not defined"
    finally:
        generate_response(content, content_type,response)


def head_handler(request, response):
    pass


def file_handler(request, response):
    pass


def delete_handler(request, response):
    pass


def generate_response(content,content_type, response):
    if content:
        response['status']= "HTTP/1.1 200 OK"
        try:
            response['Content-type'] = CONTENT_TYPE[content_type]
            response['content']      = content
        except KeyError:
            print "Content Type %r Not defined" %content_type
    else:
        response['status'] = "HTTP/1.1 404 Not Found"
    response['Date']       = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    response['Connection'] = 'close'
    response['Server']     = 'geekskool_magic_server'


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
	       }


