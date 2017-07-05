import matplotlib as mpl
mpl.use("Agg")

UNITS=''' UNITS:
Category    Variable    Units
Time    t   [ms]
Voltage v   [mV]
Current i   [mA/cm2] (distributed)
[nA] (point process)
Concentration   ko, ki, etc.    [mM]
Specific capacitance    cm  [uf/cm2]
Length  diam, L [um]
Conductance g   [S/cm2] (distributed)
[uS] (point process)
Cytoplasmic resistivity Ra  [ohm cm]
Resistance  Ri( )   [106 ohm]
'''

# pyplot is a module contained in matplotlib
import matplotlib.pyplot as plt
import numpy as np
# neuron is used as a MODULE to python
# I import it as nrn because it's clear to
# me where things come from
from neuron import h as nrn
def create_stim(seg,delay=20.,dur=100.,amp=0.05):
    # this is a neuron object with specific properties
    stim = nrn.IClamp(seg)
    stim.delay = delay
    stim.dur = dur
    stim.amp = amp

    # Returns the IClamp object
    return stim

# function to create a plot
def create_plot(data,keys=['v_PC'],name='',lim=2000, just_one=0):
    # file name specified here
    fpng = name +'ping.png'
    N=len(keys)
    # create the figure object
    fig = plt.figure(figsize=(10,5))

    # axes are listed here
    ax = {}
    for n in range(N):
        ax[keys[n]]= fig.add_subplot(N, 1, n+1)
    # plot the data here, accessing the Neuron vectors (hence the .x notation)
    # it's often useful to convert neuron vectors to numpy arrays,
    # for saving and performing operations

    for n in range(N):
        if just_one!=0:
            for i in range(just_one):
                p=ax[keys[n]].plot(data['t'], np.array(data[keys[n]][i]))
        else:
            p=ax[keys[n]].plot(data['t'], np.array(data[keys[n]]).T)
        ax[keys[n]].set_ylabel(keys[n])
        ax[keys[n]].set_xlabel('t')


    # iterate through the axis handles and set the xlims
    for axh in ax:
        ax[axh].set_xlim(0,lim)

    # now save the figure and let us know
    fig.savefig(fpng, dpi=250)
    print("Figure {} saved.".format(fpng))
    plt.show()
    # and finally do some clean up
    plt.close(fig)


def create_raster_plot(data,keys=['v_PC'], thres=[50.], name='', lim=2000):
    # file name specified here
    fpng = name +'ping.png'
    N=len(keys)
    # create the figure object
    fig = plt.figure(figsize=(10,5))

    # axes are listed here
    ax = {}
    for n in range(N):
        ax[keys[n]]= fig.add_subplot(N, 1, n+1)
    # plot the data here, accessing the Neuron vectors (hence the .x notation)
    # it's often useful to convert neuron vectors to numpy arrays,
    # for saving and performing operations

    for n in range(N):
        p=ax[keys[n]].scatter(data['t'], np.where(np.array(data[keys[n]]).T)
        ax[keys[n]].set_ylabel(keys[n])
        ax[keys[n]].set_xlabel('t')


    # iterate through the axis handles and set the xlims
    for axh in ax:
        ax[axh].set_xlim(0,lim)

    # now save the figure and let us know
    fig.savefig(fpng, dpi=250)
    print("Figure {} saved.".format(fpng))
    plt.show()
    # and finally do some clean up
    plt.close(fig)

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