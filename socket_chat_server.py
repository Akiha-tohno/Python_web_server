import socket

sk = socket.socket()
address = ('127.0.0.1', 9000)
sk.bind(address)
sk.listen(3)
print('waitting......')

while True:
    conn, addr = sk.accept()
    print('新来一个',addr)
    while True:
        data = conn.recv(1024)
        if not data:
            print('关闭了一个链接')
            conn.close()
            break
        print(str(data, 'utf8'))
        inp = input('>>>>')
        conn.send(bytes(inp, 'utf8'))