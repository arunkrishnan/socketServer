routes =  {
            'get'  : {},
            'post' : {}
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
    


