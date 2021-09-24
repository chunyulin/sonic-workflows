#!/usr/bin/env python3
import os
from os import listdir
from os.path import isfile, join

import subprocess
import sys,json,uuid
import numpy as np
from collections import defaultdict


outfile = "runs.json"

dir = subprocess.check_output('ls q* -1d', shell=True).split()
sc = np.zeros(len(dir))
for c,d in zip(sc,dir):
    c = int(d[1:])


# Parsing "[_Summary_] 4 1630771513 1630774069 9000 3.65647 3.70296 0.814144 wn14.grid.nchc.org.tw"
athput = defaultdict(list)
ethput = defaultdict(list)
node  = defaultdict(list)
wtime = defaultdict(list)
nev = defaultdict(list)

stoken = "_Summary_"
ntoken = "Running on:"
for d in dir:
    sc = int(d[1:])
    print (d, sc)
    outs = [ f for f in listdir(d) if f.endswith( ".out".encode()) ]
    
    for out in outs:
        with open( join(d, out)  ,'r') as f:
            for line in f:
                if stoken in line:
                    ls = line.split()
                    if len(ls) > 8:
                        nevent = int(ls[4])
                        if nevent<5000: continue
                        ethput[sc] += [ float(ls[5]) ]
                        athput[sc] += [ float(ls[6]) ]
                        wtime[sc]  += [ (int(ls[3]) - int(ls[2]))  ]
                        nev[sc]  += [ nevent ]
                elif ntoken in line:
                    ls = line.split()
                    node[sc] += [ int(ls[3][2:4]) ]


#print(data)


output = {
    "wtime": wtime,
    "nev": nev,
    "athput": athput,
    "ethput": ethput,
    "node": node
}

# write out
CWD = os.getcwd().split('/')[-1]
result = json.dumps(output,sort_keys=False,indent=4)
oname = "wtime_{}.json".format(CWD)
with open(oname,'w') as ofile:
    ofile.write(result)
