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


def plotStat(fname, tag):
    with open(fname, 'r') as infile:
        data = json.load(infile)

    module = list(data[tag].keys())

    fig, ax = plt.subplots()
    ax.set_xscale('log', base=10)

    for i,m in enumerate(module):
        ax.boxplot(data[tag][m], positions=[i], vert=False )

    #ax.set_yticks(range(len(module)))
    ax.set_yticklabels(module)
    ax.set_xlabel("Latency (usec): " + tag)
    #ax.yaxis.set_major_formatter(ScalarFormatter())
    #ax.set_xlim(0,32)
    #plt.legend(loc="upper left")
    
    fout = "{}_{}.png".format(fname,tag)
    plt.savefig(fout, bbox_inches='tight')

def plotCounts(fname):
    with open(fname, 'r') as infile:
        data = json.load(infile)

    module = list(data['infer_count'].keys())

    ticks = []
    fig, ax = plt.subplots()
    for i,m in enumerate(module):
        ax.boxplot(data['infer_count'][m],   positions=[i]    , vert=False )
        ax.boxplot(data['exe_count'][m],    positions=[i+0.2], vert=False )
        ax.boxplot(data['request_count'][m], positions=[i+0.4], vert=False )
        ticks += [m+'IC','EC','RC']
    
    ax.set_yticklabels(ticks)
    ax.set_xlabel("Counts")
    #ax.yaxis.set_major_formatter(ScalarFormatter())
    #ax.set_xlim(0,32)
    #plt.legend(loc="upper left")
    
    fout = "{}_{}.png".format(fname,'count')
    plt.savefig(fout, bbox_inches='tight')


for fname in sys.argv[1:]:
    plotStat(fname, "acquire")
    plotStat(fname, "produce")
    plotStat(fname, "dispatch")
    plotStat(fname, "avglatency")
    plotCounts(fname)
