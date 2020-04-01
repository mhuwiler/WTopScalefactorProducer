#!/bin/bash

echo $FILE_NAMES

python $CMSSW_BASE/src/WTopScalefactorProducer/Skimmer/newsubmission/ProductionScript.py "$GC_SCRATCH" "$FILE_NAMES" 

echo $GC_SCRATCH
ls $GC_SCRATCH

