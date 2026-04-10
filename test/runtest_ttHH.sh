#!/bin/bash

QUEUE=${1}
if [ -z ${QUEUE} ]; then
    QUEUE=local
fi

CAMPAIGNS=( "Run3Summer23wmLHE" )

if [ "$QUEUE" == "condor" ]; then
    for CAMPAIGN in "${CAMPAIGNS[@]}"; do
        crun.py test_ttHH $MYOMCPATH/test/fragment_ttHH.py ${CAMPAIGN} \
            --outEOS "/store/user/$USER/MYOMC/test/${CAMPAIGN}/$(date +"%Y-%m-%d-%H-%M-%S")/" \
            --keepMINI \
            --keepNANO \
            --nevents_job 4 \
            --njobs 4 \
            --env \
            --overwrite
    done

elif [ "$QUEUE" == "condor_eos" ]; then
    crun.py test_ttHH $MYOMCPATH/test/fragment_ttHH.py Run3Summer23wmLHE \
        --keepMINI \
        --keepNANO \
        --nevents_job 4 \
        --njobs 4 \
        --env

elif [ "$QUEUE" == "local" ]; then
    STARTDIR=$PWD
    mkdir -p testjob_tthh
    cd testjob_tthh
    source "$STARTDIR/../campaigns/Run3Summer23wmLHE/run.sh" test "$STARTDIR/fragment_ttHH.py" 4 1 1 "$STARTDIR/../campaigns/Run3Summer23wmLHE/pileupinput.dat"
    # Args are: name fragment_path nevents random_seed nthreads pileup_filelist
    cd $STARTDIR
fi