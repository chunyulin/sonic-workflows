#!/bin/bash
DAG="dagfile.dag"
rm -f $DAG

THREADS=4
CLIENTS=( 45 50 55 60 70 80 90 100 110 120 130 140 )
CLIENTS=( 280 )
N=${#CLIENTS[@]}

write_dag_job() {
    echo "JOB $1 $1.condor DIR $1" >> $DAG
}
write_dag_depend() {
    echo "PARENT $1 CHILD $2" >> $DAG
}


## prepare working folder
for (( i = 0; i < N; i++ )); do
    SUB=`printf "q%03d" ${CLIENTS[$i]}`
    #echo $SUB
    mkdir -p $SUB
    sed "s/^Queue .*/Queue ${CLIENTS[$i]}/g" tpl.condor | sed "s/_THREADS_/${THREADS}/g"  > $SUB/$SUB.condor
    
    write_dag_job $SUB
done


for (( i = 1; i < N; i++ )); do
    S0=`printf "q%03d" ${CLIENTS[$i-1]}`
    S1=`printf "q%03d" ${CLIENTS[$i]}`
    write_dag_depend $S0 $S1
done


