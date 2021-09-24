#!/usr/bin/env python3
import os
import sys,json,uuid
from collections import OrderedDict
import numpy as np
from cycler import cycler
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict
from matplotlib.ticker import ScalarFormatter

CWD = os.getcwd().split('/')[-1]
    
with open("timers_{}.json".format(CWD),'r') as infile:
    data = json.load(infile)
    
def pltTimers():
    fig, ax = plt.subplots()
    #ax.set_xscale('log', base=2)
    #ax.set_yscale('log', base=10)
    for i in data["rtime"]:
        rt = np.array(data["rtime"][i])
        tp = np.array(data["pnet"][i])
        dm = np.array(data["dmet"][i])
        dt = np.array(data["dtau"][i])
        so = (tp+dm+dt) / rt *100
        ot = np.array(data["other"][i]) / rt *100

        w = 0.3
        width = lambda p, w: 2**(np.log2(p)+w/2.)-2**(np.log2(p)-w/2.)
        
        w = 4
        #ax.boxplot(srt, positions=[int(i)], widths=width(int(i),w) )
        ax.boxplot(ot, positions=[int(i)], widths=w, showfliers = 0 )
        ax.boxplot(so, positions=[int(i)], widths=w, showfliers = 0 )
    
    
    # write fig
    oname = "timers_{}.png".format(CWD)
    ax.set_xlabel("Simutanious clients : {}".format(CWD))
    ax.set_ylabel("Time %")
    ax.xaxis.set_major_formatter(ScalarFormatter())
    #ax.set_xlim(0,32)
    #ax.set_ylim(1500,3000)
    
    plt.savefig(oname)
    
pltTimers()
