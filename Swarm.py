import math
import numpy as np # numpy so we go brr
from matplotlib import pyplot as plt
# The Swarm object for the optimization algo
# Needs a population, will spawn randomly in a given region defined by origin +/- distance
# distance will actually just set the standard deviation of a guassian distribution with mean 0.
# In 2d this will be a square and in 3D this will be a cube. In 4D... well go ask a math prof about hypercubes
# Also needs a pointer to the functional that we are minimizing and the number of params it takes
# Assuming the functional will take numerical values in an iterable object
class Swarm:

    def __init__(self, population, origin, distance, functional, params):
        self.driftVel = np.zeros((params, 1))
        self.function = functional
        self.params = params
        self.origin = origin
        self.distance = distance
        self.population = population
        self.swarmsBestPos = np.array(origin)
        self.swarmsBestVal = self.function(origin)
        assert(params == len(origin))
        self.swarm = dict()
        self.swarmPos = np.random.randn(params,population)*distance
        for i in range(params):
            self.swarmPos[i, :] += origin[i]
        self.swarmVel = np.zeros((params,population))
        self.swarmIndivBests = np.copy(self.swarmPos)
        self.swarmIndivBestVals = np.zeros(self.population)
        for i in range(self.population):
            self.swarmIndivBestVals[i] = self.function(self.swarmIndivBests[:,i])


        # now swarm is generated, guess i should add iterations

    # All weighting arrays
    def iterate(self, momentum, accelToBest, accelToGlobal):
        assert(len(momentum)==self.params)
        assert(len(accelToBest)==self.params)
        assert(len(accelToGlobal)==self.params)
        assert(np.min(accelToGlobal)>=0 and np.max(accelToGlobal)<=2)

        self.updateBests()

        # perform 1 iteration
        # update velocities
        for i in range(self.params):
            self.swarmVel[i, :] = self.swarmVel[i, :]*momentum[i] + (np.random.rand(self.population)*accelToBest[i]*(self.swarmIndivBests[i,:]-self.swarmPos[i,:])+
                                                                     np.random.rand(self.population) * accelToBest[i] * (self.swarmsBestPos[i] - self.swarmPos[i, :])
                                                                     ) + self.driftVel[i]

        # now update position
        self.swarmPos += self.swarmVel
        self.driftVel = np.zeros((self.params, 1))

    def updateBests(self):
        #lets evaluate the functionals
        evals = np.zeros(self.population)
        for i in range(self.population):
            evals[i] = self.function(self.swarmPos[:, i])
            if self.swarmIndivBestVals[i] > evals[i]:
                self.swarmIndivBests[:, i] = self.swarmPos[:, i]
                self.swarmIndivBestVals[i] = self.function(self.swarmIndivBests[:,i])

        if self.swarmsBestVal > np.min(evals):
            index = np.argmin(evals)
            self.swarmsBestPos = self.swarmPos[:, index]
            self.swarmsBestVal = self.function(self.swarmsBestPos)

    # this will only be applied to the velocity equation ONCE
    def setDriftVel(self, vels):
        self.driftVel = np.array(vels)

    def getSwarmCenter(self):
        toRet = []
        for i in range(len(self.swarmPos[:, 1])):
            toRet.append(np.sum(self.swarmPos[i, :])/self.population)
        return toRet

    # 2D functions only!
    def visualise(self):
        plt.figure(0)
        plt.clf()
        plt.quiver(self.swarmPos[0,:], self.swarmPos[1, :], self.swarmVel[0,:], self.swarmVel[1,:])

        #plt.xlim(-5, 5)
        #plt.ylim(-5,5)
        plt.draw()
        plt.pause(0.1)


