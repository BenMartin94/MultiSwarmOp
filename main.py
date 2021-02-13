import math
from Swarm import Swarm
def ackley(inpt):
    return -20*math.exp(-0.2*math.sqrt(0.5*((inpt[0]**2)+(inpt[1]**2)))) - (
        math.exp(0.5*(math.cos(2*math.pi*inpt[0])+math.cos(2*math.pi*inpt[1])))
    ) + math.exp(1)+20


opt = Swarm(100, [1,1], 3, ackley, 2)

for i in range(100):
    opt.iterate([0.5, 0.5], [0.5, 0.5],[0.5, 0.5])

print(opt.swarmsBestPos)
print(ackley(opt.swarmsBestPos))