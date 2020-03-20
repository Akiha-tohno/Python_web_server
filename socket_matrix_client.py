import numpy as np
import sys
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
c = socket(AF_INET, SOCK_STREAM)
c.connect(('localhost', 25000))
a = np.zeros(shape=50000, dtype=float)
recv_into(a, c)
print(a[0:20])
b = np.ones(shape=(100, 100), dtype=np.float32)
send_from(b, c)
#c.close()