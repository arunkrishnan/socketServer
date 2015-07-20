import socket
from pprint import pprint
import time 
import urlparse

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
	parsed_request["method"] = method.split()[0]
        parsed_request["path"] = method.split()[1]
        parsed_request["protocol"] = method.split()[2]
        header = request.split("\n\n")[0].strip()
        try:
            for each_line in header.split("\n")[1:]:
                key, value = each_line.split(":",1)
                parsed_request[key] = value
        except ValueError:
            parsed_request['content'] = request.rsplit("\n")[-1]
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
        try:
            content, content_type = Routes[path]()
        except KeyError:
            content, content_type = public(path)
 
	if content:
		response = gen_header(200)
	else:
		response = gen_header(404)
		return response
        try:
            response += "Content-type: " + Content_Type[content_type.lower()] + "\n\n"
        except KeyError:
            print "Content Type %r Not defined" %content_type

        response += content + "\n\n"

        return response

def do_POST(request):
        length = int(request['Content-Length'])
	path = request['path']
        content = urlparse.parse_qs(request['content'])
        try:
		content, content_type = Landing[path](content)
		if content:
        	        response = gen_header(200)
	        else:
               		response = gen_header(404)
                	return response
        	try:
            		response += "Content-type: " + Content_Type[content_type.lower()] + "\n\n"
        	except KeyError:
            		print "Content Type %r Not defined" %content_type

        	response += content + "\n\n"
        	return response

	except:
		pass
	raise KeyboardInterrupt


'''
*******************************************************************************
Hash Tables
'''
Routes = {"/": index,
          "/index": index,
          "/login": login,}

Landing = {"/login_submit" : login_submit,}
Methods = {'GET': do_GET,
	   'POST': do_POST,}

Content_Type = {'html': 'text/html',
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
	sock = start_server("127.0.0.1", 8080)
	sock.listen(2)
	while True:
		client, request = accept_connection(sock)
	   	if request:
			request = request_parser(request)
                	response = Methods[request['method']](request)
                	print "Sending response"
                	client.send(response)
                	client.close() 
    except KeyboardInterrupt:
	pass
            
