#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Comments are denoted by a '#'
# Shane Lee
# (c) 2012--2017
# free to use, modify, and distribute as necessary

# matplotlib provides matlab-like plotting functions
# Agg is a "backend". Others exist, for various purposes.
# See docs for more.
import matplotlib as mpl
mpl.use("Agg")

# pyplot is a module contained in matplotlib
import matplotlib.pyplot as plt

# neuron is used as a MODULE to python
# I import it as nrn because it's clear to
# me where things come from
from neuron import h as nrn
from cell import Cell
import myNeuronTools as mnt

# load neuron's runtime routine - this is critical
nrn.load_file("stdrun.hoc")

# create a cell class classes don't do anything until an instance is created


# the Pyr() class inherits from Cell().
class LTS(Cell):
    # it also has its own __init__ function
    def __init__(self):
        # FSerited classes use all the properties of the parent class
        # but they must be explicitly initialized here
        # nb this may have changed recently ...
        Cell.__init__(self)
        print self.soma.ek
        self.soma.gnabar_hh = 5.9
        self.soma.gkbar_hh = .7
        self.soma.gl_hh = 0.01
        self.soma.el_hh = -75.3
        self.soma.ena = 55
        self.soma.ek = -67

        self.syn = nrn.ExpSyn(self.soma(0.5))
        self.syn.e = 0

        # tau2 is decay
        self.syn.tau = 2

def initialize(v_init=-65):
    '''
    initializing function, setting the membrane voltages to v_init and
    resetting all state variables
    '''
    nrn.finitialize(v_init)
    nrn.fcurrent()

def integrate(tstop):
    '''
    run the simulation up until the simulation duration
    '''
    while nrn.t < tstop:
        nrn.fadvance()

# create a network, run the codes, and create a plot
def run():
    # create instance of class Network()
    cell = LTS()
    

    # compartment names for convenience.
    # here we care about the middle of the cell
 
    # create stim
    stim = cell.add_IClamp(amp=0.6)
    tstop = 200

    # creates objects of class nrn.Vector(),
    # in a dictionary
    data = {
        # time
        't': nrn.Vector(),

        # voltages will be recorded here
        'cell': nrn.Vector(),
    }

    # Record time
    data['t'].record(nrn._ref_t)

    # calls a built-in method "record" to record the voltages
    data['cell'].record(cell.segment._ref_v)

    # run the simulation (standard run)
    mnt.initialize()
    mnt.integrate(tstop)


    # use our plot routine to create the plot
    mnt.create_plot(data, name='LTS_')


if __name__ == "__main__":
    run()