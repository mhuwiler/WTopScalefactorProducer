#!/bin/bash

echo $FILE_NAMES

python $CMSSW_BASE/src/WTopScalefactorProducer/Skimmer/newsubmission/qsub_script_SFs.py "$GC_SCRATCH" "$FILE_NAMES" 

echo $GC_SCRATCH
ls $GC_SCRATCH

