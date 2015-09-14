import server
import requests
import ast
import json

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


def verify(content):
    url         = content['apiUrl'][0]
    header      = {'Authorization': ''.join(content['authHeader'])}
    data        = requests.get(url, headers=header).text
    data_dict   = ast.literal_eval(data)
    phone_num   = data_dict['phone_number']
    print phone_num
    return json.dumps({'status':'success'}),'json'
    

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
    server.add_route('get','/', home)
    server.add_route('get','/login',login)
    server.add_route('post','/verify',verify)
    server.add_route('post','/login_submit', login_submit)

    
if __name__ == "__main__":
    port = int(raw_input("PORT>")) 
    build_routes()
    server.start_server("127.0.0.1", port)
