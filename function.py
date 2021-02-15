import math
def function(inpt):
    return -20*math.exp(-0.2*math.sqrt(0.5*((inpt[0]**2)+(inpt[1]**2)))) - (
        math.exp(0.5*(math.cos(2*math.pi*inpt[0])+math.cos(2*math.pi*inpt[1])))
    ) + math.exp(1)+20