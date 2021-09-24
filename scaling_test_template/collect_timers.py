#!/usr/bin/env python3
import os
import re
from os import listdir
from os.path import isfile, join

import subprocess
import sys,json,uuid
import numpy as np
from collections import defaultdict

main = ["total", "modules", "resources" ]
net = [ "pnet", "dtau", "dmet" , "other" ]
type = dict()
type["pnet"] = ["BoostedJetONNXJetTagsProducer" , "ParticleNetSonicJetTagsProducer", "DeepFlavourONNXJetTagsProducer", "DeepDoubleXONNXJetTagsProducer" ]
type["dtau"] = ["DeepTauIdSonicProducer", "DeepTauId"]
type["dmet"] = ["DeepMETSonicProducer", "DeepMETProducer"]
type["other"] = ["other"]

def parse(fjson):

    data = json.load(open(fjson))
    nev = data["total"]["events"]

    rtime = dict()
    ctime = dict()
    for n in net:
        rtime[n] = 0
        ctime[n] = 0

    for m in data["modules"]:
        for n in net:
            if m["type"] in type[n]:
                rtime[n] += m["time_real"]
                ctime[n] += m["time_thread"]

    trtime = data["total"]["time_real"]
    tctime = data["total"]["time_thread"]

    # print("%s %f %f (%.2f%%) %f (%.2f%%) %f (%.2f%%) %f (%.2f%%)" % (cwd, trtime/nev, 
    #                                                                   rtime['pnet']/nev, rtime['pnet']/trtime*100,
    #                                                                   rtime['dtau']/nev, rtime['dtau']/trtime*100,
    #                                                                   rtime['dmet']/nev, rtime['dmet']/trtime*100,
    #                                                                   rtime['other']/nev, rtime['other']/trtime*100) )
    return trtime/nev, rtime['pnet']/nev, rtime['dtau']/nev, rtime['dmet']/nev, rtime['other']/nev



dir = subprocess.check_output('ls q* -1d', shell=True).split()
sc = np.zeros(len(dir))
for c,d in zip(sc,dir):
    c = int(d[1:])

rtime = defaultdict(list)
pnet = defaultdict(list)
dtau = defaultdict(list)
dmet = defaultdict(list)
other = defaultdict(list)

for d in dir:
    sc = int(d[1:])
    print (d, sc)
    #outs = [ f for f in listdir(d) if f.endswith( ".json".encode()) ]
    outs = [ f for f in listdir(d) if f.startswith("result_sonic_".encode()) ]
    
    for out in outs:
        res = parse( join(d, out) )
        
        rtime[sc]  += [ res[0]  ]
        pnet[sc]   += [ res[1]  ]
        dtau[sc]   += [ res[2] ]
        dmet[sc]   += [ res[3] ]
        other[sc]  += [ res[4] ]

output = {
    "rtime": rtime,
    "pnet": pnet,
    "dtau": dtau,
    "dmet": dmet,
    "other": other
}

# write out
CWD = os.getcwd().split('/')[-1]
result = json.dumps(output,sort_keys=False,indent=4)
oname = "timers_{}.json".format(CWD)
with open(oname,'w') as ofile:
    ofile.write(result)

