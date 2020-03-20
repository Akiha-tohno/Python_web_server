import  socket

sk = socket.socket()
address = ('127.0.0.1', 9000)
sk.connect(address)
while True:
    inp = input('>>>>')
    if inp == 'exit':
        break
    sk.send(bytes(inp, 'utf8'))
    data = sk.recv(1024)
    print(str(data, 'utf8'))
else:
    sk.close()