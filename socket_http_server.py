import socket
import urllib.parse
import json
import time
def save(data,path):
    s=json.dumps(data,indent=2,ensure_ascii=False)
    f=open(path,'w+',encoding='utf-8')
    print('save',path,s)
    f.write(s)

def load(path):
    f=open(path,'r',encoding='utf-8')
    s=f.read()
    return json.loads(s)

class Model(object):
    @classmethod
    #得到指定类名的txt文件名
    def db_path(cls):
        class_name=cls.__name__
        path='{}.txt'.format(class_name)
        return path
    @classmethod
    def all(cls):
        path=cls.db_path()
        models=load(path)
        ms=[cls(m) for m in models]
        return ms
    def save(self):
        models=self.all()
        models.append(self)
        l=[m.__dict__ for m in models]
        path=self.db_path()
        save(l,path)

class User(Model):
    def __init__(self,form):
        self.username=form.get('username','')
        self.password=form.get('password','')
    def validate_login(self):
        path=self.db_path()
        models=load(path)
        for i in models:
            if i['username']==self.username and i['password']==self.password:
                return True
        return False
    def validate_register(self):
        return len(self.username)>2 and len(self.password)>2


class Request(object):
    #初始化
    def __init__(self):
        self.path=''
        self.query={}
        self.method='GET'#默认get
        self.body=''
    def form(self):
        #url编码 ascll 不能用中文
        body=urllib.parse.unquote(self.body)
        log('body ',body)
        #message=1&author=2
        args=body.split('&')
        f={}
        for arg in args:
            k,v=arg.split('=')
            f[k]=v
        return f

def run(host='',port=3000):
        s=socket.socket()
    #with socket.socket as s:
        s.bind((host,port))
        while True:
            s.listen(3)
            connection,address=s.accept()
            print(address)
            r=connection.recv(1024)
            r=r.decode('utf-8')#bytes to str
            #print(r)
            #GET /message?message=1&author=2 HTTP/1.1
            if len(r.split())<2:
                continue
            #try:
            request.method=r.split()[0]
            request.body=r.split('\r\n\r\n')[1]
            path=r.split()[1]
            response=response_for_path(path)
            connection.sendall(response)
            #except Exception as e:
            #    log('error',e)
            connection.close()

def response_for_path(path):
    path,query=parsed_path(path)
    request.path=path
    request.query=query
    log('path and query',path,query)
    r={
        '/':route_index,
        '/login':route_login,
        '/register':route_register,
        '/sdqe':route_sdqe,
        '/img/sdqe.gif':route_img_sdqe,
        '/i19':route_i19,
        '/img/i19.gif':route_img_i19,
        '/all':route_all,
        '/message':route_message,
        '/hello':route_hello,
    }
    response=r.get(path,error)
    if path == '/login' or path=='/register':
        return response(request)
    else:
        return response()

def parsed_path(path):
    index=path.find('?')
    if index==-1:
        #no '?'
        return path,{}
    else:
        path,query_s=path.split('?',1)
        args=query_s.split('&')
        query={}
        for arg in args:
            k,v=arg.split('=')
            query[k]=v
        return path,query

def log(*args,**kwargs):
    print(*args,**kwargs)



request=Request()
message_list=[]

def template(filename):
    f=open(filename,'r',encoding='utf-8')
    return f.read()

def route_index():
    header='HTTP/1.1 220 OK\r\nContent-Type: text/html\r\n'
    body=template('./templates/index.html')
    r=header+'\r\n'+body
    return r.encode(encoding='utf-8')#str to bytes

def route_login(request):
    header='HTTP/1.1 220 OK\r\nContent-Type: text/html\r\n'
    if request.method=='POST':
        form=request.form()
        u=User(form)
        if u.validate_login():
            result='welcome'
        else:
            result='Login failed'
    else:
        result=''
    body=template('./templates/login.html')
    body=body.replace('{{result}}',result)
    r=header+'\r\n'+body
    return r.encode(encoding='utf-8')


def route_register(request):
    header='HTTP/1.1 220 OK\r\nContent-Type: text/html\r\n'
    if request.method=='POST':
        form=request.form()
        u=User(form)
        if u.validate_register():
            u.save()
            result='registration success'
        else:
            result='registration failed'
    else:
        result=''
    body=template('./templates/register.html')
    body=body.replace('{{result}}',result)
    r=header+'\r\n'+body
    return r.encode(encoding='utf-8')


def route_hello():
    header='HTTP/1.1 220 OK\r\nContent-Type: text/html\r\n'
    body='<h1>Hello World!</h1>'
    r=header+'\r\n'+body
    return r.encode(encoding='utf-8')#str to bytes

def route_sdqe():
    header='HTTP/1.1 220 OK\r\nContent-Type: text/html\r\n'
    body='<h1>Hello World!</h1><img src="img/sdqe.gif" />'
    r=header+'\r\n'+body
    return r.encode(encoding='utf-8')

def route_i19():
    header='HTTP/1.1 220 OK\r\nContent-Type: text/html\r\n'
    body='<h1>Hello World!</h1><img src="img/i19.gif" />'
    r=header+'\r\n'+body
    return r.encode(encoding='utf-8')

def route_all():
    header='HTTP/1.1 220 OK\r\nContent-Type: text/html\r\n'
    body='<h1>Hello World!</h1><img src="img/sdqe.gif" /><img src="img/i19.gif" />'
    r=header+'\r\n'+body
    return r.encode(encoding='utf-8')

def route_img_sdqe():
    #with open('sdqe.jpg','rb') as f:
    f=open('./images/sdqe_1.jpg','rb')
    header=b'HTTP/1.1 220 OK\r\nContent-Type: image/jpg\r\n'
    img=header+b'\r\n'+f.read()
    return img

def route_img_i19():
    #with open('sdqe.jpg','rb') as f:
    f=open('./images/i19.gif','rb')
    header=b'HTTP/1.1 220 OK\r\nContent-Type: image/gif\r\n'
    img=header+b'\r\n'+f.read()
    return img

class Message(object):
    def __init__(self):
        self.message=''
        self.author=''
    
    def __repr__(self):
        return '{} : {}'.format(self.author,self.message)

def route_message():
    if request.method=='POST':
        msg=Message()
        form=request.form()
        msg.author=form.get('author','')
        msg.message=form.get('message','')
        message_list.append(msg)
    header='HTTP/1.1 210 OK\r\nContent-Type:text/html\r\n'
    body=template('./templates/message.html')
    msgs='<br>'.join([str(m) for m in message_list])
    body=body.replace('{{message}}',msgs)
    r=header+'\r\n'+body
    return r.encode(encoding='utf-8')


def error(code=404):
    error_dict={
        404:b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>404 NOT FOUND</h1>',
        405:b''
    }
    return error_dict.get(code,b'')
    #r=header+'HTTP/1.1 404 NOT FOUND\r\n\r\n'+template('templates/404/index.html')
    #return r.encode(encoding='utf-8')

#config=dict(
#    host='',
#    port=3000,
#)
#run(**config)
run('',3000)

