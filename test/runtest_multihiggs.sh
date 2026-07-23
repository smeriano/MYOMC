#!/bin/bash

QUEUE=${1}
if [ -z "${QUEUE}" ]; then
    QUEUE=local
fi


# SEED_OFFSET=0
# NJOBS=100

# Change seed offest if you dont want to run on the same files!
SEED_OFFSET=10
NJOBS=1
NEVENTS_PER_JOB=100

CAMPAIGN_NAMES=("Run3Summer23wmLHE")

FRAGMENT_FILES=(
    "fragment_ggHHH_kt_1p0_k3_8p164_k4_m52p932_Run3Summer24NanoAODv15_1.py"
    # "fragment_ttHH_2B2Tau_SM.py"
    # "fragment_ttHH_2B2Tau_opt_0.py"
    # "fragment_ttHH_2B2Tau_opt_1.py"
    # "fragment_ttHH_2B2Tau_opt_2.py"
    # "fragment_ttHH_2B2Tau_opt_3.py"
    # "fragment_ttHH_2B2Tau_opt_4.py"
)

if [ "${QUEUE}" == "condor" ]; then
    for CAMPAIGN_NAME in "${CAMPAIGN_NAMES[@]}"; do
        for FRAGMENT_FILE in "${FRAGMENT_FILES[@]}"; do
            SAMPLE_NAME=$(basename "${FRAGMENT_FILE}" .py)
            SEED_END=$((SEED_OFFSET + NJOBS - 1))

            OUTPUT_DIR="/eos/user/s/$USER/MYOMC_output/test/${CAMPAIGN_NAME}/${SAMPLE_NAME}/seeds_${SEED_OFFSET}_${SEED_END}/"

            crun.py "${SAMPLE_NAME}" "$MYOMCPATH/test/${FRAGMENT_FILE}" "${CAMPAIGN_NAME}" \
                --outEOS "${OUTPUT_DIR}" \
                --keepNANO \
                --nevents_job "${NEVENTS_PER_JOB}" \
                --njobs "${NJOBS}" \
                --seed_offset "${SEED_OFFSET}" \
                --max_nthreads 1 \
                --env \
                --overwrite
        done
    done

    # --keepMINI   # Uncomment if you want MiniAOD output

elif [ "$QUEUE" == "local" ]; then
    STARTDIR=$PWD
    mkdir -p testjob_tthh_local
    cd testjob_tthh_local || exit 1
    source "$STARTDIR/../campaigns/Run3Summer23wmLHE/run.sh" test "$STARTDIR/fragment_ttHH_2B2Tau_SM.py" 3 1 1 "$STARTDIR/../campaigns/Run3Summer23wmLHE/pileupinput.dat"
    # Args are: name fragment_path nevents random_seed nthreads pileup_filelist
    cd "$STARTDIR" || exit 1
fi