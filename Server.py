import socket
import time
import threading
import numpy
import random
import traceback
workers = []
HOST = '192.168.0.7'
PORT = 9998

def manageWorker(connection):
    global activeWorkers
    global inpt
    global start
    global OPT
    global ALLRESULTS
    # TODO maybe set up an observer design pattern to only send when a change is detected
    connection.sendall(b'Hey worker, standby')
    try:
        while True:
            connection.sendall(inpt.encode('utf-8'))
            if inpt == OPT:
                while '-0' in start:
                    time.sleep(0.1) # the input hasnt been given yet so wait
                randStart = randomize(start)
                connection.sendall(randStart.encode('utf-8'))
                time.sleep(5)
                results = (connection.recv(1024))
                results = results.decode('utf-8')
                print(results) # TODO delete me
                results = results.split(' ')
                ALLRESULTS[tuple(results[0:-1])] = results[-1]
            time.sleep(1)
    except:
        # something happened, down a worker
        traceback.print_exc()
        print("Thread crashed closing client connection")
        activeWorkers = activeWorkers-1

def randomize(given):
    given = given.split(' ')
    toRet = ''
    for i in range(len(given)):
        possiblities = [int(given[i])*0.5, int(given[i])*1.5]
        given[i] = int(random.randrange(min(possiblities), max(possiblities)))
        toRet += str(given[i]) + ' '

    toRet = toRet[0:-1]
    return toRet


def listen():
    global activeWorkers
    global ALLTHREADS
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST,PORT))
        s.listen(5)
        print('listening')
        while True:
            c, addr = s.accept()
            if 'Work' in str(c.recv(1024)):
                print('client connected, starting thread for it')
                activeWorkers = activeWorkers+1
                x = threading.Thread(target=manageWorker, args=(c,))
                ALLTHREADS.append(x)
                x.daemon=True
                x.start()

OPT = '1'
IDLE = '0'
WORKERS = '2'
ALLTHREADS = []
ALLRESULTS = {}
activeWorkers = 0
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
            print('Sorry you got not workers')
            inpt = IDLE
            continue
        start = input("Enter starting coordinates (ints only right now)")
        print("Ordering workers, just wait")
        time.sleep(2)
        print("Workers should be goin hard")
        inpt = IDLE
        start = '-0 -0'
        while len(ALLRESULTS)<activeWorkers:
            # results not rdy
            time.sleep(0.5)
        print('This is what the workers found')
        print(ALLRESULTS)
        ALLRESULTS = {}
    elif inpt == WORKERS:
        print("There are " + str(activeWorkers) + ' workers connected')
        inpt = IDLE
    inpt = input()
print('Killing the threads')
for thread in ALLTHREADS:
    thread.join(0.01)
print('Killed the listener')
