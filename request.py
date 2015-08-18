import socket
import urllib

def request_stringify(request):
    response = 'GET ' + request['path'] + ' HTTP/1.1\r\n'
    for key in request['header']:
        response += key + ': ' + request['header'][key] + '\r\n'
    response+='\r\n'
    try:
        response += request['body'] + '\r\n'
    except:
        pass
    print response
    return response    

def get(url, auth, path='/', port=80):
    request                              = {}
    request['header']                    = {}
    request['header']['Authorization']   = auth
    request['path']                      = "/".join(url.split("/")[3:])  
    request['header']['Host']            = "/".join(url.split("/")[:3]) + ':' + str(port)
    request['header']['Accept']          = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    request['header']['Accept-Language'] = 'en-US,en;q=0.5'
    request['header']['Accept-Encoding'] = 'gzip, deflate'
    request['header']['Connection']      = 'keep-alive'
 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('api.digits.com',80))
    sock.send(request_stringify(request))
    data = sock.recv(1024)
    sock.close()
    return data
   
def post(url,body="", port=8080):
    request                              = {}
    request['header']                    = {}
    request['path']                      = "/".join(url.split("/")[3:])
    print request['path']
    request['header']['Host']            = url + ':' + str(port)
    request['header']['Contect-type']    = 'application/x-www-form-urlencoded'
    request['header']['Accept']          = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    request['header']['Accept-Language'] = 'en-US,en;q=0.5'
    request['header']['Accept-Encoding'] = 'gzip, deflate'
    request['header']['Connection']      = 'keep-alive'
    print body 
#    params                               = urllib.urlencode(body)
    request['body']                      = body
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((url,port))
    sock.send(request_stringify(request))
    data = sock.recv(1024)
    sock.close()
    return data

