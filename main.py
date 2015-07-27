import server

def home():
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
           result = home()
           return result
    except:
        pass
        return '',''

def build_routes():
    server.routes('get','/', home)
    server.routes('get','/index',home)
    server.routes('get','/login',login)
    server.routes('post','/login_submit', login_submit)

    
if __name__ == "__main__":
    port = 8080
    build_routes()
    sock = server.start_server("127.0.0.1", port)
