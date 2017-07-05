#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Comments are denoted by a '#'
# Shane Lee
# (c) 2012--2017
# free to use, modify, and distribute as necessary

# modules are imported to extend functionality
# itertools is a module that supplies fast iteration routines
import itertools as it

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

# load neuron's runtime routine - this is critical
nrn.load_file("stdrun.hoc")

from FS import FS
from LTS import LTS
from PC import PC
import numpy as np
import myNeuronTools as mnt
# the Network() class creates the network
class Network():
    def __init__(self, Np=21, Nf=3, Nl=3,size=(1.,1.)):
        # these are lists in python
        self.PC_list = []
        self.FS_list = []
        self.LTS_list = []

        self.size = size
        # master connect list for all synapses
        # a place to store things that I'm not keeping very carefully
        # because I won't need to refer to them again, I just need them
        # to exist in memory
        self.nc_list = []

        # this calls a method of this class, defined below, to create cells
        self.create_cells(Np,'PC')
        self.create_cells(Nl,'LTS')
        self.create_cells(Nf,'FS')

        self.connect_distance_pair(self.PC_list, self.PC_list, b=0.015, c=3.,k=.31)
        self.connect_distance_pair(self.PC_list, self.FS_list, b=0.005, c=3.,k=.2)
        self.connect_distance_pair(self.FS_list, self.PC_list, b=0.002, c=3., k=-.05)
        self.connect_distance_pair(self.PC_list, self.LTS_list, b=0.005, c=1.5,k=1.8)
        self.connect_distance_pair(self.LTS_list, self.PC_list, b=0.015, c=1.5, k=-.15)
        #self.connect_distance_pair(self.LTS_list, self.FS_list, b=0.005, c=5.4, k=-1.)
        #self.connect_distance_pair(self.FS_list, self.LTS_list, b=0.002, c=5.4)

        # set to record spikes
        self.spiketimes = nrn.Vector()
        self.spikegids = nrn.Vector()
        self.__record_spikes()

    # Creating cells is this easy
    def create_cells(self,N,cell='PC'):
        # even though we are only simulating one of each cell, this structure
        # enables you the ability to simulate more cells and keep them separate
        for i in range(N):
            if cell == 'PC':
                self.PC_list.append(eval(cell+'()'))
            if cell == 'LTS':
                self.LTS_list.append(eval(cell+'()'))
            if cell == 'FS':
                self.FS_list.append(eval(cell+'()'))

    def connect_distance_pair(self, pop_1, pop_2,b,c,k=.5):
        # Create PC<->PC Connections
        for cell_i, cell_o in it.product(pop_1, pop_2):
            d = np.sqrt((cell_i.x-cell_o.x)**2+(cell_i.y-cell_o.y)**2+(cell_i.z-cell_o.z)**2)
            p = c/(1+np.exp(d-b))
            if np.random.rand(1)<p:
                self.nc_list.append(cell_i.connect_to_target(cell_o.syn))

                # depends on synapse being connected to (mS)
                # only for this ExpSyn and Exp2Syn cases!
                self.nc_list[-1].weight[0] = 1e-3*(p+np.random.random()*.05)*k
                self.nc_list[-1].delay = d

    

# create a network, run the codes, and create a plot
if __name__ == "__main__":
    # create instance of class Network()
    # Density: 79 cells/mm2, 109 cells/mm3 -> 200 cells / 79 = 1.59x1.59x0.72mm
    net = Network(Np=200,Nf=25,Nl=25,size=(1.59,1.59))
    tstop = 2000
    # compartment names for convenience.
    # here we care about the middle of the cell
    # creates objects of class nrn.Vector(),
    # in a dictionary
    data = {
    # time
    't': nrn.Vector(),
    # voltages will be recorded here
    'v_PC': [],
    'v_FS': [],
    'v_LTS': [],
    'stim': [],
    'PC'
    'spk_PC': nrn.Vector(),
    }

    for i, cell in enumerate(net.PC_list):
        # compartment names for convenience.
        # here we care about the middle of the cell    seg_e = net.cell_list_e[0].soma(0.5)
        data['v_PC'].append(nrn.Vector())
        # calls a built-in method "record" to record the voltages
        data['v_PC'][i].record(cell.segment._ref_v)
        # create stim
        data['stim'].append(cell.add_random_spikes())
    for i, cell in enumerate(net.FS_list):
        # compartment names for convenience.
        # here we care about the middle of the cell    seg_e = net.cell_list_e[0].soma(0.5)
        data['v_FS'].append(nrn.Vector())
        # calls a built-in method "record" to record the voltages
        data['v_FS'][i].record(cell.segment._ref_v)
        # create stim
        # data['stim'].append(cell.add_random_spikes())
    for i, cell in enumerate(net.LTS_list):
        # compartment names for convenience.
        # here we care about the middle of the cell    seg_e = net.cell_list_e[0].soma(0.5)
        data['v_LTS'].append(nrn.Vector())
        # calls a built-in method "record" to record the voltages
        data['v_LTS'][i].record(cell.segment._ref_v)
        # create stim
        # data['stim'].append(cell.add_random_spikes())
    keys = ['v_PC', 'v_FS','v_LTS']
    # Record time
    data['t'].record(nrn._ref_t)

    # ecell current - an example of recording other currents
    # itest = nrn.Vector()
    # itest.record(seg_e._ref_ina)

    # run the simulation (standard run)
    mnt.initialize()
    mnt.integrate(tstop)


    # use our plot routine to create the plot
    mnt.create_plot(data,name='multi_PC_',keys=keys,just_one=5)
