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

tags   = ['g1_t4v', 'g1_t4', 'g2_t4v' , 'g2_t4', 'g4_t4v', 'g4_t4', 'm3_t4v', 'm3_t4'  ]
color = ['k--', 'k.-', 'r--', 'r.-' , 'g--' , 'g.-'  , 'm--' , 'm.-' ]

tags   = ['direct_t4', 'g1_t4', 'g2_t4' , 'g4_t4'  , 'g8_t4' , 'm3_t4', 'PR10/g1_t4'  ]
color = ['k.-', 'g.-', 'r.-', 'b.-' , 'm.-.' , 'y.-' , 'g--' ]

tags   = ['direct_t4', 'g1_t4', 'g2_t4' , 'g4_t4'  , 'g8_t4' , 'm3_t4', 'PR10/g1_t4'  ]
color = ['k', 'g.-', 'r.-', 'b.-' , 'm.-' , 'y.-' , 'g--' ]


dat="sync_tput.dat"

BASE=4.97267   ### avg ev/s from 20 direct_t4 runs

def aggRelativeImprove(fout):
    
    tags   = ['direct_t4', 'g1_t4', 'g2_t4' , 'g4_t4', 'm3_t4'  ]
    color = ['k', 'g.-', 'r.-', 'b.-' , 'y.-']

    """
    Compare against the first colume
    """
    
    sc = np.array([1, 10, 20, 30, 40 ])

    data0 = np.loadtxt("{}/{}".format(tags[0],dat))
    d0 = data0[np.in1d(data0[:,0], sc)]
    print(d0)
    
    plt.figure()
    plt.axhline(y=0, linestyle='--', color='k')
    #for i in range(1,len(tags)):
    for tag,c in zip(tags,color):
        data = np.loadtxt("{}/{}".format(tag,dat))
        d1 = data[np.in1d(data[:,0],sc)]
        print(d1)
        #plt.plot(sc, (d1[:,1]-d0[:,1])/d0[:,1]*100, 'o-', label=tags[i], markersize=5, linewidth=1)
        plt.plot(sc, (d1[:,1]-BASE*sc)/(BASE*sc)*100, c, label=tag, markersize=5, linewidth=1)

    plt.xlabel("Simultaneous (submit) clients")
    plt.ylabel("% changes against direct_t4")
    plt.grid()
    plt.legend()
    plt.savefig(fout, dpi=100, bbox_inches='tight')


def aggScale(fout):
    
    plt.figure()
    for tag,c in zip(tags,color):
        print(tag)
        data = np.loadtxt("{}/{}".format(tag,dat))

        plt.plot(data[:,3], data[:,1], c, label=tag, markersize=5, linewidth=1)

    plt.axvline(x=140, ls="--")
    plt.xlim(0,110)
    plt.ylim(0,400)

    plt.xlabel("Simultaneous clients")
    plt.ylabel("ev / s")
    #plt.grid()
    plt.legend(loc="upper left")
    plt.savefig(fout, dpi=100, bbox_inches='tight')

def avgScale(fout):
    
    tags   = ['direct_t4', 'g1_t4', 'g2_t4' , 'g4_t4', 'm3_t4'  ]
    color = ['k', 'g.-', 'r.-', 'b.-' , 'y.-']

    plt.figure()
    for tag,c in zip(tags,color):
        print(tag)
        data = np.loadtxt("{}/{}".format(tag,dat))

        plt.plot(data[:,3], data[:,1]/data[:,3], c, label=tag, markersize=5, linewidth=1)

    #plt.axvline(x=140, ls="--")
    plt.axhline(y=4.97267, ls="--", color='k')

    plt.xlim(0,110)
    plt.ylim(2.0,5.5)

    plt.xlabel("Simultaneous clients")
    plt.ylabel("Avg. ev/s")
    plt.grid()
    plt.legend(loc="lower right")
    plt.savefig(fout, dpi=100, bbox_inches='tight')

def aggScaleE(fout):
    
    plt.figure()
    for tag,c in zip(tags,color):
        print(tag)
        data = np.loadtxt("{}/{}".format(tag,dat))

        plt.plot(data[:,0], data[:,2], '.-', color=c, label=tag, markersize=5, linewidth=0.5)

    #plt.xlim(0,80)
    #plt.ylim(0,400)

    plt.xlabel("Simultaneous clients")
    plt.ylabel("ev / sec")
    plt.grid()
    plt.legend(loc="upper left")
    plt.savefig(fout, dpi=100, bbox_inches='tight')




aggScale("scalingA.png")
avgScale("scaling_avgA.png")
aggRelativeImprove("scaling_rel.png")
#aggScaleE("scalingE.png")


