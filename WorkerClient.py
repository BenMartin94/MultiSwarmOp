import socket
import time
from Swarm import Swarm
from function import function
HOST = '192.168.0.7'
PORT = 9999



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Worker')

    while True:
        resp = (s.recv(1024)).decode('utf-8')
        #print(resp)
        if resp == '1':
            print('Beginning Optimizaiton')
            start = (s.recv(1024)).decode('utf-8')
            start = start.split(' ')
            for i in range(len(start)):
                start[i] = int(start[i])
            print("beginning search at: ")
            print(start)
            opt = Swarm(1000, start, (max(start)*0.2), function, len(start))
            for i in range(1000):
                opt.iterate([0.9, 0.9], [0.4, 0.4], [0.2, 0.2])
            #time.sleep(5) # make sure that the server is ready to recieve info again
            toSend = ''
            for num in opt.swarmsBestPos:
                toSend+=str(num).strip()+' '
            toSend+=str(opt.swarmsBestVal)
            s.sendall(toSend.encode('utf-8'))
            print('Sent: ' + toSend)
            print("Found minimum at: ")
            print(opt.swarmsBestPos)
        if not resp:
            break

