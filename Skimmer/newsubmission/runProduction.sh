#!/bin/bash

python $CMSSW_BASE/src/WTopScalefactorProducer/Skimmer/newsubmission/qsub_script_SFs.py $FILE_NAMES

echo $GC_SCRATCH
ls $GC_SCRATCH

