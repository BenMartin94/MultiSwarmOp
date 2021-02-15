import socket
import time
from Swarm import Swarm
from function import function
HOST = '127.0.0.1'
PORT = 9999



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Worker')

    while True:
        resp = (s.recv(1024)).decode('utf-8')
        print(resp)
        if resp == '1':
            print('Beginning Optimizaiton')
            start = (s.recv(1024)).decode('utf-8')
            start = start.split(' ')
            for i in range(len(start)):
                start[i] = int(start[i])
            print(start)
            opt = Swarm(100, start, (max(start)*0.2), function, len(start))
            for i in range(100):
                opt.iterate([0.9, 0.9], [0.4, 0.4], [0.2, 0.2])
            #time.sleep(5) # make sure that the server is ready to recieve info again
            s.sendall(opt.swarmsBestPos.tobytes())

        if not resp:
            break

