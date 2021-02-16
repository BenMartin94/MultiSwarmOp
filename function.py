import math
'''
def function(inpt):
    return -20*math.exp(-0.2*math.sqrt(0.5*((inpt[0]**2)+(inpt[1]**2)))) - (
        math.exp(0.5*(math.cos(2*math.pi*inpt[0])+math.cos(2*math.pi*inpt[1])))
    ) + math.exp(1)+20

'''

def function(inpt):
    x = inpt[0]
    y = inpt[1]
    return ((x+2*y-7)**2)+(2*x+y-5)**2