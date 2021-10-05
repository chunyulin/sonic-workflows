#!/bin/bash
CLIENTS=( 30 25 20 15 10 5  1 )  ## number of simultanious clients
REPEATS=( 1  1  1  1  2  2 10 )  ## repeat times for each CLIENTS...
THREADS=4

#### ===========================================================================
DAG="dagfile.dag"
rm -f $DAG

N=${#CLIENTS[@]}

write_dag_job() {
    echo "JOB $1 $2.condor DIR $2" >> $DAG
    echo "SCRIPT POST $1 echo" >> $DAG
}
write_dag_depend() {
    echo "PARENT $1 CHILD $2" >> $DAG
}


## prepare working folder
J0=""
for (( i = 0; i < N; i++ )); do

    FOLDER=`printf "q%03d" ${CLIENTS[$i]}`
    mkdir -p $FOLDER

    R=${REPEATS[$i]}
    for (( j = 0; j < R; j++ )); do

        sed "s/^Queue .*/Queue ${CLIENTS[$i]}/g" tpl.condor | sed "s/_THREADS_/${THREADS}/g"  > $FOLDER/$FOLDER.condor

        JID=`printf "q%03d_%02d" ${CLIENTS[$i]} ${j}`
        write_dag_job $JID $FOLDER

        ## set dependence
        [ ! -z "$J0" ] && write_dag_depend $J0 $JID
        J0=$JID
        echo  >> $DAG
    done
done
