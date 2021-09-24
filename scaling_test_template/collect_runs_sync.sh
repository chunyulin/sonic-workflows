#!/bin/bash

OUT=runs.dat
> ${OUT}

summarize_runs() {   ## $1 = simultanious clients
    
    LIST=`ls -1 $1/*.out`

    for f in $LIST; do
        ERR=${f/.out/.err}

	##NEV=`tail result_sonic.json | grep "events" | awk '{print $2}'`
        #HOST=`grep "Running on: " ${f} | awk '{print $4}'`
        #NODE=${HOST:2:2}
        ATPUT=`grep 'Average ' ${ERR} | awk '{print $3,$5}'`
        T=`grep _Summary_  ${f} | awk '{print $3,$4}'`
        TPUT=-1 ##`grep ' Event Throughput: ' ${ERR}| awk '{print $3}'`
        NEV=`grep "_Summ" ${f} | awk '{print $5}'`
        NODE=`grep "_Summ" ${f} | awk '{print $9}'`

        if [ ! -z "$ATPUT" ]; then
    	 echo ${NEV} ${TPUT} ${ATPUT} ${T} ${NODE} $1
        fi
    done
}

SUBS=`ls q* -d`





####################################
OUT=runs.dat
echo "# Ev passed, Ev/s from Timer report (no used), Avg ev/s, Std of Avg ev/s, T0, T1, Exec node, Running folder" >${OUT}

#CLIENTS=( 1 10 15 20 25 30 35 40 50 )
#N=${#CLIENTS[@]}
for SUB in $SUBS; do
    #SUB=`printf "q%03d" ${CLIENTS[$i]}`
    summarize_runs $SUB  | tee -a ${OUT}
done


####################################
OUT2=sync_tput.dat
echo "# Submit clients, Aggregate ev/s, Ev/s from Timer report (no used), Successful clients" >${OUT2}

#N=${#CLIENTS[@]}
#for (( i = 0; i < N; i++ )); do
for SUB in $SUBS; do
    #SUB=`printf "q%03d" ${CLIENTS[$i]}`
    SUCCRUN=`grep Summ ${SUB}/*.out | wc -l`
    if (( SUCCRUN > 0 )); then
        grep $SUB ${OUT} | awk  '{sume += $2; sum += $3} END {print "'"${SUB:1}"'", sum, sume, "'"${SUCCRUN}"'" }' | tee -a ${OUT2}
    fi
done


