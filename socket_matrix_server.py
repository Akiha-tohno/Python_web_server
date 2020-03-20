import sys
import numpy as np
from socket import *

def send_from(arr, dest):
    view = memoryview(arr).cast('B')
    while len(view):
        nsent = dest.send(view)
        view = view[nsent:]
def recv_into(arr, source):
    view = memoryview(arr).cast('B')
    while len(view):
        nrecv = source.recv_into(view)
        view = view[nrecv:]

s = socket(AF_INET, SOCK_STREAM)
s.bind(('', 25000))
s.listen(1001)
time = 0
while True:
    print("time ", time)
    c, a = s.accept()
    a = np.arange(0.0, 500000.0)
    send_from(a, c)

    array = np.zeros(shape=(100, 100), dtype=np.float32)
    recv_into(array, c)
    print(array[0])
    time += 1