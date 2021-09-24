#!/usr/bin/env python3
import os
import re
import sys,json,uuid
import numpy as np
from collections import defaultdict
import itertools


def parseTagBlock(f, tag):
    """
    Return lines start with tag
    """
    found = 0
    res=''
    while True:
        l = f.readline()
        if not l:
            yield res
            break
    
        if l.startswith(tag):
            if found:
                yield res
            else:
                found = 1
            res = l
        else:
            if found:
                res += l

#%MSG-i DeepMETSonicProducer:  DeepMETSonicProducer:deepMETsResponseTune  13-Sep-2021 23:06:22 CST Run: 1 Event: 7356
#dispatch() time: 987192
pattern1 = re.compile("%MSG-i (\w+):\s+(\w+):(\w+)  \d{2}-.*\n(\w*)\(\) time: (\d+)", re.MULTILINE)
#%MSG-i DeepMETSonicProducer:TritonClient:  (NoModuleName)  13-Sep-2021 23:06:24 CST pre-events
#  Inference count: 34
#  Execution count: 28
#  Successful request count: 34
#  Avg request latency: 21464 usec
#  (overhead 73 usec + queue 5813 usec + compute input 161 usec + compute infer 15406 usec + compute output 11 usec)
pattern2 = re.compile("""%MSG-i (\w+):TritonClient:  \(NoModuleName\)  \d{2}-.*
  Inference count: (\d+)
  Execution count: (\d+)
  Successful request count: (\d+)
  Avg request latency: (\d+) usec
  \(overhead (\d+) usec \+ queue (\d+) usec \+ compute input (\d+) usec \+ compute infer (\d+) usec \+ compute output (\d+) usec\)
""", re.MULTILINE)


"""
class ClientStat:
    def __init__(self):
        self.tag = ""
        self.acquire = []
        self.produce = []
        self.dispatch = []
    def put(self, match):
        if      match.group(4) == "acquire":
            match.group(4) 
        else if match.group(4) == "prouce":
        else    match.group(4) == "dispatch":
"""

cli_a = defaultdict()
cli_d = defaultdict()
cli_p = defaultdict()
ser_ic = defaultdict()
ser_ec = defaultdict()
ser_rc = defaultdict()
ser_al = defaultdict()

ser_oh = defaultdict()
ser_qu = defaultdict()
ser_ci = defaultdict()
ser_cf = defaultdict()
ser_co = defaultdict()

output = {
    "dispatch":cli_d,
    "acquire":cli_a,
    "produce":cli_p,
    
    "infer_count":ser_ic,
    "exe_count":ser_ec,
    "request_count":ser_rc,
    
    "avglatency": ser_al,
    "overhead": ser_oh,
    "queue": ser_qu,
    "cin": ser_ci,
    "cinfer": ser_cf,
    "cout": ser_co
}

for fname in sys.argv[1:]:

    ## consistency check
    if not fname.endswith(".err"):
        break

    with open(fname) as f:

        for piece in parseTagBlock(f, "%MSG"):

            match = re.search(pattern1, piece)
            if match:
                module = match.group(3)
                type = match.group(4)
                time = match.group(5)
                if module not in cli_d.keys():
                    cli_d[module] = []
                    cli_a[module] = []
                    cli_p[module] = []
                
                if type=="acquire":   cli_a[module].append(int(time))
                if type=="dispatch":  cli_d[module].append(int(time))
                if type=="produce":   cli_p[module].append(int(time))
                continue
            
            match = re.search(pattern2, piece)
            if match:
                module = match.group(1)
                if (module) not in ser_rc.keys():
                    ser_ic[module] = []
                    ser_ec[module] = []
                    ser_rc[module] = []
                    ser_al[module] = []
                    
                    ser_oh[module] = []
                    ser_qu[module] = []
                    ser_ci[module] = []
                    ser_cf[module] = []
                    ser_co[module] = []
                
                ser_ic[module].append(int( match.group(2) ))
                ser_ec[module].append(int( match.group(3) ))
                ser_rc[module].append(int( match.group(4) ))
                ser_al[module].append(int( match.group(5) ))
                
                ser_oh[module].append(int( match.group(6) ))
                ser_qu[module].append(int( match.group(7) ))
                ser_ci[module].append(int( match.group(8) ))
                ser_cf[module].append(int( match.group(9) ))
                ser_co[module].append(int( match.group(10) ))
                continue

        ## write out
        result = json.dumps(output,sort_keys=False,indent=4)
        oname = fname.replace(".err", ".json")
        with open(oname,'w') as ofile:
            ofile.write(result)


            
#print (client)
#print (ser_ic)
#fig, ax = plt.subplots()
#mo = [next(g) for _, g in itertools.groupby(cli.keys(), key=lambda x:x[0])]




#print( list(dict(list_ofs).items())    )
#ax.boxplot(ot, positions=[int(i)], widths=w, showfliers = 0 )
        




    