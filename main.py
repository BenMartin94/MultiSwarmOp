import math
from Swarm import Swarm
def ackley(inpt):
    return -20*math.exp(-0.2*math.sqrt(0.5*((inpt[0]**2)+(inpt[1]**2)))) - (
        math.exp(0.5*(math.cos(2*math.pi*inpt[0])+math.cos(2*math.pi*inpt[1])))
    ) + math.exp(1)+20
def booth(inpt):
    x = inpt[0]
    y = inpt[1]
    return ((x+2*y-7)**2)+(2*x+y-5)**2
opt = Swarm(100, [1,1], 3, booth, 2)

for i in range(100):
    opt.iterate([0.9, 0.9], [0.4, 0.4],[0.2, 0.2])
    opt.visualise()

print(opt.swarmsBestPos)
print(ackley(opt.swarmsBestPos))