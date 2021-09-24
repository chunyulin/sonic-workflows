#!/usr/bin/env python3
import sys,json,uuid
from collections import defaultdict


main = ["total", "modules", "resources" ]
net = [ "pnet", "dtau", "dmet" , "other" ]

type = dict()
type["pnet"] = ["BoostedJetONNXJetTagsProducer" , "ParticleNetSonicJetTagsProducer", "DeepFlavourONNXJetTagsProducer", "DeepDoubleXONNXJetTagsProducer" ]
type["dtau"] = ["DeepTauIdSonicProducer", "DeepTauId"]
type["dmet"] = ["DeepMETSonicProducer", "DeepMETProducer"]
type["other"] = ["other"]

import os
def parse(fjson):

    cwd    = fjson.split('/')[-2]
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

    #print("Total {:6.1f}  {:4.0f} %".format( trtime/nev, 100 ) )
    #for n in net:
    #        print("{:5s} {:6.1f}  {:4.1f} %".format( n, rtime[n]/nev, rtime[n]/trtime*100) )
    #print("Sum   {:6.1f}  {:4.1f} %".format( sum(rtime.values())/nev, sum(rtime.values())/trtime*100) )
    
    print("%s %f %f (%.2f%%) %f (%.2f%%) %f (%.2f%%) %f (%.2f%%)   %f " % (cwd, trtime/nev, 
                                                                       rtime['pnet']/nev, rtime['pnet']/trtime*100,
                                                                       rtime['dtau']/nev, rtime['dtau']/trtime*100,
                                                                       rtime['dmet']/nev, rtime['dmet']/trtime*100,
                                                                       rtime['other']/nev, rtime['other']/trtime*100,
                                                                       tctime/nev )
                                                                        )
    #print("%s %f %f %f %f" % (cwd, tctime/nev, ctime['pnet']/nev, ctime['dtau']/nev, ctime['dmet']/nev) )

for f in sys.argv[1:]:
    parse(f)

