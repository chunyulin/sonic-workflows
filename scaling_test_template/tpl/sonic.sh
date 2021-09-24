#!/bin/bash
RUNID=$1
CORE=$2


### 1)　Prepare env
T0=`date +%s`
echo "Running on: `uname -a`"
source /cvmfs/cms.cern.ch/cmsset_default.sh

tar -xf /scratch/sonic_data/sonic_PR13.tgz

cd CMSSW_12_0_0_pre5/src/
SRC=`pwd`

scramv1 b -r ProjectRename # this handles linking the already compiled code - do NOT recompile
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
echo "====== Setup done in $((`date +%s`-$T0)) secs"
#sleep $[ ( $RANDOM % 500 )  + 1 ]s

 
### 2) cmsRun
cd sonic-workflows

T0=`date +%s`
cmsRun run.py maxEvents=9000 threads=${CORE} verbose=False tmi=False address="203.145.219.187" port=56482 #sonic=false
T1=`date +%s`
echo "====== cmsRun done in $(($T1-$T0)) secs"


### 3) postProcessing
rm -f *.root
NEV=`tail result_sonic.json | grep "events" | awk '{print $2}'`
mv result_sonic.json ${_CONDOR_SCRATCH_DIR}/result_sonic_${RUNID}.json

cd ${_CONDOR_SCRATCH_DIR}
ATPUT=`grep 'Average ' _condor_stderr | awk '{print $3,$5}'`
TPUT="-1"     #`grep " Event Throughput: " _condor_stderr| awk '{print $3}'`
NODE=`hostname`
echo [_Summary_] ${CORE} ${T0} ${T1} ${NEV::-1} ${TPUT} ${ATPUT} ${NODE:2:2}
