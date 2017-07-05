#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Comments are denoted by a '#'
# Shane Lee
# (c) 2012--2017
# free to use, modify, and distribute as necessary

# modules are imported to extend functionality
# itertools is a module that supplies fast iteration routines

# neuron is used as a MODULE to python
# I import it as nrn because it's clear to
# me where things come from
from neuron import h as nrn
import numpy as np

# load neuron's runtime routine - this is critical
nrn.load_file("stdrun.hoc")

# create a cell class classes don't do anything until an instance is created
class Cell():
    # functions/definitions are defined within a function
    # __init__ is a special function that is called when an instance of a class is created
    # if there are inputs to this class, they would go here in the __init__
    # not in the class def above. See class documentation for more.
    def __init__(self, pos=[-1,-1]):
        # neuron provides a Section() class that we use to create a soma
        # and we can use built-ins to give it properties
        self.soma = nrn.Section()
        self.soma.insert('hh')
        self.soma.diam = 10
        self.soma.L = 10
        self.segment = self.soma(0.5)

        if pos[0]==-1:
            pos[0]=np.random.random()*1.59
        if pos[1]==-1:
            pos[1]=np.random.random()*1.59
        self.x = pos[0]
        self.y = pos[1]
        self.z = np.random.random()*0.72
        nrn.pt3dadd(self.x*1000.,self.y*1000.,self.z*1000.,self.soma.diam)

    def add_IClamp(self, delay=25., dur=100., amp=0.05):
        '''Generates IClamp step input current'''
        self.stim = nrn.IClamp(self.segment)
        self.stim.delay = delay
        self.stim.dur = dur
        self.stim.amp = amp

        # Returns the IClamp object
        return self.stim
    def add_random_spikes(self):
        '''Generates random spiking activity entering the synapse'''
        ns = nrn.NetStim(0.5)  # spike time generator object (~presynaptic)
        ns.noise = 1.               # Fractional randomness (intervals from exp dist)
        ns.start = 25.               # approximate time of first spike
        ns.number = 500            # number of spikes
        ns.interval = 500.           # average interspike interval
        nc = nrn.NetCon(ns, self.syn)  # Connect generator to synapse
        nc.weight[0] = .01           # Set synapse weight

        # Returns the IClamp object
        return nc,ns

        
    # general function we will use here to create a NetCon object
    def connect_to_target(self, synapse):
        # event generated, to where delivered
        nc = nrn.NetCon(self.soma(0.5)._ref_v, synapse, sec=self.soma)
        nc.threshold = 0.

        return nc
    

# create a network, run the codes, and create a plot
if __name__ == "__main__":
    pass
