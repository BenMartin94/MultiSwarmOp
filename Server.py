import socket
import time
import threading
import numpy as np
import random
import traceback
from function import function
workers = []
HOST = '10.0.1.12'
PORT = 9999

def manageWorker(connection):
    global activeWorkers
    global inpt
    global start
    global OPT
    global ALLRESULTS
    global ALLPOSITIONS
    # TODO maybe set up an observer design pattern to only send when a change is detected
    connection.sendall(b'Hey worker, standby')
    myId = workerID
    try:
        while True:
            connection.sendall(inpt.encode('utf-8'))
            if inpt == OPT:
                while '-0' in start:
                    time.sleep(0.1) # the input hasnt been given yet so wait
                randStart = randomize(start)
                connection.sendall(randStart.encode('utf-8'))
                connection.sendall('0 0'.encode('utf-8'))  # TODO generalize this to n dimensions
                response = connection.recv(1024).decode('utf-8')
                while "DONE" not in response:
                    respList = response.split(' ')
                    for i in range(len(respList)):
                        respList[i] = float(respList[i])
                    ALLPOSITIONS[myId] = respList
                    driftVel = computeDrift(myId)
                    # Send something back now
                    toSend = ''
                    for val in driftVel:
                        toSend += str(val) + ' '
                    toSend = toSend[:-1]
                    connection.sendall(toSend.encode('utf-8'))
                    response = connection.recv(1024).decode('utf-8')

                results = response[4:len(response)]
                results = results.split(' ')
                ALLRESULTS[tuple(results[0:-1])] = results[-1]
            time.sleep(1)
    except:
        # something happened, down a worker
        traceback.print_exc()
        ALLPOSITIONS.pop(myId)  # this worker disappeared so lets drop this entry
        print("Thread crashed closing client connection")
        activeWorkers = activeWorkers-1

def randomize(given):
    given = given.split(' ')
    toRet = ''
    for i in range(len(given)):
        possiblities = [int(given[i])*0.5, int(given[i])*1.5]
        given[i] = int(random.randrange(int(min(possiblities)), int(max(possiblities))))
        toRet += str(given[i]) + ' '

    toRet = toRet[0:-1]
    return toRet

def computeDrift(myId):
    #if id is even, this will be a convergent based swarm
    global ALLPOSITIONS
    dims = len(ALLPOSITIONS[myId])//2
    toRet = []
    for i in range(dims):
        toRet.append(0)
    if myId % 2 == 0:
        dest = None
        myMin = np.inf
        for bests in list(ALLPOSITIONS.values()):
            if function(bests[0:dims])<myMin:
                myMin = function(bests[0:dims])
                dest = np.array(bests[0:dims])

        org = np.array(ALLPOSITIONS[myId][dims:dims*2])
        distance = np.linalg.norm(dest-org, dims)
        for i in range(dims):
            toRet[i] = (dest[i] - org[i])

    else:
        for pos in list(ALLPOSITIONS.values()):
            # i want the second half of pos to get the swarm center
            me = np.array(ALLPOSITIONS[myId][dims:len(pos)])
            other = np.array(pos[dims:len(pos)])
            distance = np.linalg.norm(other - me, dims)
            if 1 > distance > 0:
                # too close!
                for i in range(dims):
                    toRet[i] = (me[i] - other[i])/distance

    return toRet


def listen():
    global activeWorkers
    global ALLTHREADS
    global workerID
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST,PORT))
        s.listen(5)
        print('listening')
        while True:
            c, addr = s.accept()
            if 'Work' in str(c.recv(1024)):
                print('client connected, starting thread for it')
                activeWorkers = activeWorkers+1
                workerID+=1
                x = threading.Thread(target=manageWorker, args=(c,))
                ALLTHREADS.append(x)
                x.daemon=True
                x.start()

OPT = '1'
IDLE = '0'
WORKERS = '2'
ALLTHREADS = []
ALLRESULTS = {}
ALLPOSITIONS = {}
activeWorkers = 0
workerID = 0
start = '-0 -0'
listener = threading.Thread(target=listen)
listener.daemon=True
listener.start()
ALLTHREADS.append(listener)
inpt = IDLE
time.sleep(1)
print("Enter a q to quit\nEnter a 1 to begin optimizing")
inpt = input("Give Commands now: \n")
while inpt != 'q':
    if inpt == OPT:
        if activeWorkers == 0:
            print('Sorry you got no workers')
            inpt = IDLE
            continue
        start = input("Enter starting coordinates (ints only right now)")
        print("Ordering workers, just wait")
        time.sleep(0.5)
        print("Workers should be goin hard")
        inpt = IDLE
        start = '-0 -0'
        while len(ALLRESULTS)<activeWorkers:
            # results not rdy
            time.sleep(0.5)
        print('This is what the workers found')
        for key in ALLRESULTS:
            print("f" + str(key)+" = " + str(ALLRESULTS[key]))
        ALLRESULTS = {}
    elif inpt == WORKERS:
        print("There are " + str(activeWorkers) + ' workers connected')
        inpt = IDLE
    inpt = input()
print('Killing the threads')
for thread in ALLTHREADS:
    thread.join(0.01)
print('Killed the listener')
