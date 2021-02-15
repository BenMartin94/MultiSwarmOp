import socket
import time
import threading
import numpy
workers = []
HOST = '127.0.0.1'
PORT = 9999

def manageWorker(connection):
    global activeWorkers
    global inpt
    global start
    global OPT
    connection.sendall(b'Hey worker, standby')
    try:
        while True:
            connection.sendall(inpt.encode('utf-8'))
            if inpt == OPT:
                while '-0' in start:
                    time.sleep(0.1) # the input hasnt been given yet so wait
                # TODO call a randomizer function here to spread out swarms
                connection.sendall(start.encode('utf-8'))
                time.sleep(5)
                results = (connection.recv(1024))
                print(numpy.frombuffer(results))
            time.sleep(1)
    except:
        # something happened, down a worker
        activeWorkers = activeWorkers-1
def listen():
    global activeWorkers
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST,PORT))
        s.listen(5)
        print('listening')
        while True:
            c, addr = s.accept()
            if 'Work' in str(c.recv(1024)):
                print('client connected, starting thread for it')
                activeWorkers = activeWorkers+1
                threading.Thread(target=manageWorker, args=(c,)).start()

OPT = '1'
IDLE = '0'
WORKERS = '2'
activeWorkers = 0
start = '-0 -0'
threading.Thread(target=listen).start()
inpt = IDLE
time.sleep(1)
print("Enter a q to quit\nEnter a 1 to begin optimizing")
inpt = input("Give Commands now: \n")
while inpt != 'q':
    if inpt == OPT:
        start = input("Enter starting coordinates (ints only right now)")
        print("Ordering workers, just wait")
        time.sleep(5)
        print("Workers should be goin hard")
        inpt = IDLE
    elif inpt == WORKERS:
        print("There are " + str(activeWorkers) + ' workers connected')
        inpt = IDLE
    inpt = input()