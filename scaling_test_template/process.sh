#!/bin/bash

LIST=`ls -1 *.out`

for f in $LIST; do
    ERR=${f/.out/.err}

    HOST=`grep "Running on: " ${f} | awk '{print $4}'`
    NODE=${HOST:2:2}
    ATPUT=`grep 'Average ' ${ERR} | awk '{print $3,$5}'`
    T=`grep _Summary_  ${f} | awk '{print $3,$4}'`
    TPUT=`grep ' Event Throughput: ' ${ERR}| awk '{print $3}'`
    NEV=`grep " passed = " ${ERR} | awk '{print $8}'`

    if [ ! -z "$ATPUT" ]; then
	 echo ${NEV} ${TPUT} ${ATPUT} ${T} ${NODE}
    fi
    #echo [_Summary_] ${CORE} ${T0} ${T1} ${ENV} ${TPUT} ${ATPUT}

done