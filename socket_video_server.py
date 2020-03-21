import socket
import urllib.parse
import json
import time
import cv2
#import matplotlib
#import matplotlib.pyplot as plt
#import io

class Request(object):
    #初始化
    def __init__(self):
        self.path=''
        self.query={}
        self.method='GET'
        self.body=''
    def form(self):
        #url ascll
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
        s.bind((host,port))
        while True:
            s.listen(3)
            connection,address=s.accept()
            print(address)
            r=connection.recv(4096)
            r=r.decode('utf-8')#bytes to str
            #GET /message?message=1&author=2 HTTP/1.1
            if len(r.split())<2:
                continue
            #try:
            request.method=r.split()[0]
            request.body=r.split('\r\n\r\n')[1]
            path=r.split()[1]
            if parsed_path(path)[0] == '/kancolle':
                header=b'HTTP/1.1 220 OK\r\nContent-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n'
                connection.sendall(header)
                for i in range(159):
                    #b=plt.imread('1/'+str(i)+'.png')
                    #buf = io.BytesIO()
                    #matplotlib.pyplot.imsave(buf,b,format='PNG')
                    #body = buf.getvalue()
                    img = cv2.imread('kancolle_png/'+str(i)+'.png')
                    #success, arr = cv2.imencode(".png", img)
                    body = cv2.imencode(".png", img)[1].tobytes()
                    r=b'--frame\r\nContent-Type: image/png\r\n\r\n'+body
                    connection.sendall(r)
                    time.sleep(0.03)
                connection.close()
            elif parsed_path(path)[0]=='/fubuki':
                header=b'HTTP/1.1 220 OK\r\nContent-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n'
                connection.sendall(header)
                for i in range(85):
                    #b=plt.imread('1/'+str(i)+'.png')
                    #buf = io.BytesIO()
                    #matplotlib.pyplot.imsave(buf,b,format='PNG')
                    #body = buf.getvalue()
                    img = cv2.imread('shirakami_fubuki_png/'+str(i)+'.png')
                    #success, arr = cv2.imencode(".png", img)
                    body = cv2.imencode(".png", img)[1].tobytes()
                    r=b'--frame\r\nContent-Type: image/png\r\n\r\n'+body
                    connection.sendall(r)
                    time.sleep(0.03)
                connection.close()                
            else:
                response=response_for_path(path)
                connection.sendall(response)
                connection.close()

def response_for_path(path):
    path,query=parsed_path(path)
    request.path=path
    request.query=query
    log('path and query',path,query)
    r={
        '/hello':route_hello,
    }
    response=r.get(path,error)
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

def route_hello():
    header='HTTP/1.1 220 OK\r\nContent-Type: text/html\r\n'
    body='<h1>Hello World!</h1>'
    r=header+'\r\n'+body
    return r.encode(encoding='utf-8')#str to bytes

def error(code=404):
    error_dict={
        404:b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>404 NOT FOUND</h1>',
        405:b''
    }
    return error_dict.get(code,b'')

request=Request()
run('',3000)