#!/usr/bin/env python3
import os
import re
import sys,json,uuid
import numpy as np
from collections import defaultdict
import itertools

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict
from matplotlib.ticker import ScalarFormatter


with open(sys.argv[1], 'r') as f:
    d1 = json.load(f)
with open(sys.argv[2], 'r') as f:
    d0 = json.load(f)

mclient = list(d0['acquire'].keys())
mserver = list(d0['queue'].keys())

metrics = ['avglatency','overhead','queue','cin','cinfer','cout']
me_cli =  ['acquire','produce','dispatch']

def hboxplot(data, positions, c, fliers = False):
    plt.boxplot(data, positions=positions, vert=False, showfliers=fliers, widths=0.3,
        boxprops=dict(color=c),
        capprops=dict(color=c),
        whiskerprops=dict(color=c),
        flierprops=dict(color=c, markeredgecolor=c),
        medianprops=dict(color=c)   )


def cmpServerStat(d1, d0):

    module = list(d1['queue'].keys())

    fig, ax = plt.subplots()
    ax.set_xscale('log', base=10)

    xticks = []
    p = 0
    for mo in module:
        for me in metrics:
            hboxplot(d0[me][mo], positions=[p],     c='k' )
            hboxplot(d1[me][mo], positions=[p+0.4], c='r' )
            p+=1
            xticks += [ "{}: {}".format(mo,me), ' ' ]
        p+=1

    #ax.set_yticks(range(len(module)))
    ax.set_yticklabels(xticks)
    ax.set_xlabel("Latency (usec): ")
    #ax.yaxis.set_major_formatter(ScalarFormatter())
    #ax.set_xlim(0,32)
    #plt.legend(loc="upper left")
    
    fout = "comapre_server.png"
    plt.savefig(fout, bbox_inches='tight')

def cmpClientStat(d1, d0):

    module = list(d1['dispatch'].keys())

    fig, ax = plt.subplots()
    ax.set_xscale('log', base=10)

    xticks = []
    p = 0
    for mo in module:
        for me in me_cli:
            hboxplot(d0[me][mo], positions=[p],     c='k' )
            hboxplot(d1[me][mo], positions=[p+0.4], c='r' )
            p+=1
            xticks += [ "{}: {}".format(mo,me), ' ' ]
        p+=1
        
    ax.set_yticklabels(xticks)
    ax.set_xlabel("Latency (usec): ")
    
    fout = "comapre_client.png"
    plt.savefig(fout, bbox_inches='tight')

def cmpCountStat(d1, d0):

    me_count =  ['request_count','exe_count','infer_count']
    module = list(d1['exe_count'].keys())

    fig, ax = plt.subplots()
    ax.set_xscale('log', base=10)

    xticks = []
    p = 0
    for mo in module:
        for me in me_count:
            hboxplot(d0[me][mo], positions=[p],     c='k',fliers = True )
            hboxplot(d1[me][mo], positions=[p+0.4], c='r',fliers = True )
            p+=1
            xticks += [ "{}: {}".format(mo,me), ' ' ]

        #r0 = np.array(d0['infer_count'][mo])/np.array(d0['exe_count'][mo])
        #r1 = np.array(d1['infer_count'][mo])/np.array(d1['exe_count'][mo])
        #hboxplot(r0, positions=[p],     c='k',fliers = True )
        #hboxplot(r1, positions=[p+0.4], c='r',fliers = True )
        #p+=1
        #xticks += [ "{}: {}".format(mo,"inf/exe"), ' ' ]
        
        p+=1
        
    ax.set_yticklabels(xticks)
    ax.set_xlabel("Counts")
    
    fout = "comapre_count.png"
    plt.savefig(fout, bbox_inches='tight')


cmpServerStat(d1, d0)
cmpClientStat(d1, d0)
cmpCountStat(d1, d0)
