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
            opt = Swarm(100, start, (max(start)*0.2), function, len(start))
            for i in range(100):
                driftVel = s.recv((1024)).decode('utf-8')
                driftVel = driftVel.split(' ')
                for i in range(len(driftVel)):
                    driftVel[i] = float(driftVel[i])
                opt.setDriftVel(driftVel)
                opt.iterate([0.9, 0.9], [0.4, 0.4], [0.2, 0.2])
                # send back the minimum postition followd by the swarmCenter
                toSend = ''
                for i in range(len(opt.swarmsBestPos)):
                    toSend += str(opt.swarmsBestPos[i])+ " "
                center = opt.getSwarmCenter()
                for i in range(len(center)):
                    toSend += str(center[i])+" "
                toSend = toSend[:-1]  # drop the last space
                s.sendall(toSend.encode('utf-8'))
            s.send("DONE".encode('utf-8'))
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

