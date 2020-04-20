#!/bin/bash

echo $FILE_NAMES

env

python $CMSSW_BASE/src/WTopScalefactorProducer/Skimmer/newsubmission/ProductionScript.py "$GC_SCRATCH" "$FILE_NAMES" 

# Additional manual copying of file for safety
# /scratch/mhuwiler/Wtagging/production/${GC_TASK_ID}/${DATASETPATH}/
destinationpath=/work/mhuwiler/data/WScaleFactors/production/${GC_TASK_ID}/${DATASETPATH}/

mkdir -p $destinationpath

cp $GC_SCRATCH/out.root $destinationpath/job_${GC_JOB_ID}_out.root
cp $GC_SCRATCH/qualitycheck.pkl $destinationpath/job_${GC_JOB_ID}_qualitycheck.pkl
cp $GC_SCRATCH/timing.dat $destinationpath/job_${GC_JOB_ID}_timing.dat

echo $GC_SCRATCH
ls -l $GC_SCRATCH

