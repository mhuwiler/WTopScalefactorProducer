#!/bin/bash

echo $FILE_NAMES

env


WD=/afs/cern.ch/work/m/mhuwiler/software/cc7/Wtagging/CMSSW_10_2_6/src/WTopScalefactorProducer/Skimmer/newsubmission

cd $WD

#export SCRAM_ARCH=slc7_amd64_gcc700           #### Better to work on CC7 than SL6
#export X509_USER_PROXY=${HOME}/private/x509up

source env.sh

source /cvmfs/cms.cern.ch/cmsset_default.sh
cd ${CMSSW_BASE}/src
eval `scramv1 runtime -sh`

cd $WD


python $CMSSW_BASE/src/WTopScalefactorProducer/Skimmer/newsubmission/ProductionScript.py "$GC_SCRATCH" "$FILE_NAMES" 

# Additional manual copying of file for safety
# /scratch/mhuwiler/Wtagging/production/${GC_TASK_ID}/${DATASETPATH}/
destinationpath=/eos/home-m/mhuwiler/data/Wtagging/production/${GC_TASK_ID}/${DATASETPATH}/

mkdir -p $destinationpath

cp $GC_SCRATCH/out.root $destinationpath/job_${GC_JOB_ID}_out.root
cp $GC_SCRATCH/qualitycheck.pkl $destinationpath/job_${GC_JOB_ID}_qualitycheck.pkl
cp $GC_SCRATCH/timing.dat $destinationpath/job_${GC_JOB_ID}_timing.dat

echo $GC_SCRATCH
ls -l $GC_SCRATCH

