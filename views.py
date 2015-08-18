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
           result = index()
           return result
    except:
        pass
        return '',''

