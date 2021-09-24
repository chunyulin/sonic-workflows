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
    
with open("wtime_{}.json".format(CWD),'r') as infile:
    data = json.load(infile)
    
stat = defaultdict(list)


def pltAggTP():
    ####  Aggregate tput
    fig, ax = plt.subplots()
    #ax.set_xscale('log', base=2)
    tp="athput"
    for i in data[tp]:
        stp = np.array(data[tp][i])
        print(i,np.sum(stp))
        ax.plot(int(i), np.sum(stp), 'ko' )
    
    # write fig
    oname = "tp_{}.png".format(CWD)
    ax.set_xlabel("Simutanious clients : {}".format(CWD))
    ax.set_ylabel("Aggrate ev/s")
    ax.xaxis.set_major_formatter(ScalarFormatter())
    plt.savefig(oname)

def pltWalltime():
    fig, ax = plt.subplots()
    ax.set_xscale('log', base=2)
    wt="wtime"
    nv="nev"
    #stat[k] = defaultdict(list)
    for i in data[wt]:
        swt = np.array(data[wt][i])
        snv = np.array(data[nv][i])
        swt = swt / snv*9000

        w = 0.3
        width = lambda p, w: 2**(np.log2(p)+w/2.)-2**(np.log2(p)-w/2.)
        
        ax.boxplot(swt, positions=[int(i)], widths=width(int(i),w) )
    
    # write fig
    oname = "wtime_{}.png".format(CWD)
    ax.set_xlabel("Simutanious clients : {}".format(CWD))
    ax.set_ylabel("WTime for 9000 ev")
    #ax.set_xlim(0,32)
    #ax.set_ylim(1500,3000)
    ax.xaxis.set_major_formatter(ScalarFormatter())
    
    plt.savefig(oname)
    
pltAggTP()
pltWalltime()
