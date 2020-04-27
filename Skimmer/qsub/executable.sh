#!/bin/bash 
                        
#Set your simulation directory 

CURRDIR=${pwd} #/eos/home-m/mhuwiler/software/cc7/CMSSW_10_2_6/src/WTopScalefactorProducer/Fitter/partiallyMerged/jobfactory

RUNDIR=/tmp/mhuwiler/singlejob

#. /cvmfs/sft.cern.ch/lcg/releases/LCG_94/ROOT/6.14.04/x86_64-slc6-gcc62-opt/ROOT-env.sh

mkdir -p "$RUNDIR"

#Run your program 

#python runSF_nanoAOD.py "$@"

#Save your results 

#cp $RUNDIR/output.root ${CURRDIR} 

echo "Hello" > outputtest.dat

cp -r $RUNDIR ${CURRDIR} 

#cp $RUNDIR/plots.root ${CURRDIR}

#cp $RUNDIR/TMVAClassification_BDT.weights.xml ${CURRDIR}

#cp $RUNDIR/TMVAClassification_BDT.class.C ${CURRDIR}

rm -r $RUNDIR


