#!/usr/bin/env python3
import os
import sys
import numpy as np
import matplotlib
import matplotlib as mpl
matplotlib.use('Agg')
matplotlib.rcParams.update({'font.size': 12})
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.gridspec as gridspec

CWD = os.getcwd().split('/')[-1]

fin = "runs.dat"
if len(sys.argv) >1:
    fin = sys.argv[1]

#9000 0.650769 0.645608 0.139928 1630548813 1630562700
from collections import defaultdict


def timeline(fin, fout):
    data = np.loadtxt(fin, usecols=(0,1,2,3,4,5,6))

    fig, ax = plt.subplots(2,1,sharex=True,figsize=(6,8), gridspec_kw={'height_ratios': [1, 4]})
    fig.subplots_adjust(hspace=0)
    ax1 = ax[0]
    ax2 = ax[1]

    tmin=min(data[:,4])
    tmax=max(data[:,5])
    n=tmax-tmin
    node = data[:,6]
    #pmin=min(data[:,2])
    #pmax=max(data[:,2])
    colors = cm.rainbow(np.linspace(0, 1, int(max(node))))

    yc=np.zeros(int(n))
    for d in data:
        dt = d[5]-d[4]
        for i in range(int(d[4]),int(d[5])):
            yc[int(i-tmin)] += 1
    ax[0].plot(yc,'k', linewidth=1)
    ax[0].set_ylabel("Counts")
    
    for d in data:
        tp   = d[2]
        c    = int(d[6])-1
        
        ax[1].hlines(y=tp, xmin=d[4]-tmin, xmax=d[5]-tmin, 
                color=colors[c], linewidth=1)
        ax[1].plot(d[4]-tmin, tp,'ko',  markersize=1) 
    
    ax[1].set_xlabel("Timeline (s). {} jobs of {}".format(len(data), CWD) )
    ax[1].set_ylabel("ev/s")
    ax1.grid()
    ax2.grid()
    plt.savefig(fout, dpi=200, bbox_inches='tight')
    


def throughput_scaling(fin, fout):
    data = np.loadtxt(fin, usecols=(0,1,2,3,4,5,6))

    tmin=int(min(data[:,4]))
    tmax=int(max(data[:,5]))
    n=tmax-tmin
    yc=np.zeros(n)
    yt=np.zeros(n)
    for d in data:
        dt = d[5]-d[4]
        tp = d[2]
        for i in range(int(d[4]),int(d[5])):
            yc[i-tmin] += 1
            yt[i-tmin] += tp

    plt.figure()
    plt.plot(yc, yt, '.', label=CWD, markersize=1)
    plt.xlabel("Simultaneous clients")
    plt.ylabel("Aggregate ev/s")
    plt.grid()
    plt.legend(loc="upper left")
    plt.savefig(fout, dpi=100, bbox_inches='tight')

def throughput_scaling_with_hist(fin, fout):

    fig, ax = plt.subplots(2,1,sharex=True,figsize=(6,6), gridspec_kw={'height_ratios': [1, 5]})
    fig.subplots_adjust(hspace=0)
    ax1 = ax[0]
    ax2 = ax[1]

    data = np.loadtxt(fin, usecols=(0,1,2,3,4,5,6))

    tmin=int(min(data[:,4]))
    tmax=int(max(data[:,5]))
    n=tmax-tmin
    yc=np.zeros(n)
    yt=np.zeros(n)
    for d in data:
        dt = d[5]-d[4]
        tp = d[2]
        for i in range(int(d[4]),int(d[5])):
            yc[i-tmin] += 1
            yt[i-tmin] += tp

    max_clients = int(max(yc))

    hist = ax1.hist(yc, bins=0.5+np.array( range(max_clients+1) )  )   ## [1,2,3,...,max(yc)+1]
    
    ax1.set_ylabel("Counts")
    ax2.plot(yc, yt, '.', label=CWD, markersize=1)
    ax2.set_xlabel("Simultaneous clients")
    ax2.set_ylabel("Aggregate ev/s")
    #ax2.set_xlim([0,max_clients])

    plt.grid()
    plt.legend(loc="upper left")
    plt.savefig(fout, dpi=100, bbox_inches='tight')

timeline(fin, "timeline_{}.png".format(CWD))
throughput_scaling_with_hist(fin, "scale_{}.png".format(CWD))
##runtime_scaling(fin, "rt_{}.png".format(CWD))


